from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = "Initialize PostgreSQL JWT extensions, secret, and helper function"

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def handle(self, *args, **options):
        secret = getattr(settings, "SECRET_KEY", None)
        if not secret:
            raise CommandError(
                "settings.SECRET_KEY is empty or not set. Aborting."
            )

        steps = [
            ("Installing pgcrypto extension",    self._step_pgcrypto),
            ("Installing pgjwt extension",        self._step_pgjwt),
            ("Setting session-level JWT secret",  self._step_set_config),
            ("Persisting JWT secret (ALTER SYSTEM)", self._step_alter_system),
            ("Reloading PostgreSQL config",        self._step_reload_conf),
            ("Creating decode_jwt_with_key()",     self._step_create_function),
        ]

        self.stdout.write(self.style.MIGRATE_HEADING("Initializing JWT database setup …\n"))

        for i, (label, fn) in enumerate(steps, start=1):
            self.stdout.write(f"  [{i}/{len(steps)}] {label} …", ending=" ")
            try:
                fn(secret)
                self.stdout.write(self.style.SUCCESS("✔"))
            except CommandError:
                self.stdout.write(self.style.ERROR("✘"))
                raise
            except Exception as exc:
                self.stdout.write(self.style.ERROR("✘"))
                raise CommandError(f'Step "{label}" failed: {exc}') from exc

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✔  JWT database initialisation complete."))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _run_sql(self, sql: str, params=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, params)

    def _fetch_one(self, sql: str, params=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    # ------------------------------------------------------------------
    # Steps
    # ------------------------------------------------------------------

    def _step_pgcrypto(self, secret: str):
        self._run_sql("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    def _step_pgjwt(self, secret: str):
        self._run_sql("CREATE EXTENSION IF NOT EXISTS pgjwt;")

    def _step_set_config(self, secret: str):
        """
        Sets the secret for the current session.
        Using %s parameterisation keeps the secret out of query logs.
        """
        self._run_sql(
            "SELECT set_config('myapp.jwt_secret', %s, false);",
            [secret],
        )

    def _step_alter_system(self, secret: str):
        """
        Persists the secret across restarts via ALTER SYSTEM.
        ALTER SYSTEM cannot be parameterised, so we use mogrify to safely
        escape the value before embedding it in the DDL string.
        """
        with connection.cursor() as cursor:
            # Safely escape the secret value via the DB driver
            escaped = cursor.mogrify("%s", [secret]).decode()
            cursor.execute(
                f"ALTER SYSTEM SET myapp.jwt_secret = {escaped};"
            )

    def _step_reload_conf(self, secret: str):
        self._run_sql("SELECT pg_reload_conf();")

    def _step_create_function(self, secret: str):
        ddl = """
            CREATE OR REPLACE FUNCTION decode_jwt_with_key(
                token text,
                alg   text DEFAULT 'HS256'
            )
            RETURNS jsonb
            LANGUAGE plpgsql
            STABLE
            AS $func$
            DECLARE
                result       record;
                payload_json jsonb;
                secret       text;
                exp_epoch    bigint;
                now_epoch    bigint := FLOOR(
                                 EXTRACT(EPOCH FROM clock_timestamp())
                             )::bigint;
            BEGIN
                -- 1. Load secret from Postgres settings
                BEGIN
                    secret := current_setting('myapp.jwt_secret', true);
                EXCEPTION
                    WHEN OTHERS THEN
                        RAISE EXCEPTION
                        USING ERRCODE = '22023',
                              MESSAGE = 'JWT error: secret not configured '
                                        '(set myapp.jwt_secret)';
                END;

                -- 2. Validate token input
                IF token IS NULL OR length(token) < 10 THEN
                    RAISE EXCEPTION
                    USING ERRCODE = '22023',
                          MESSAGE = 'JWT error: token missing or too short';
                END IF;

                -- 3. Verify signature
                result := verify(token, secret, alg);

                IF result.valid IS DISTINCT FROM TRUE THEN
                    RAISE EXCEPTION
                    USING ERRCODE = '22023',
                          MESSAGE = 'JWT error: signature mismatch '
                                    '(wrong secret, token altered, '
                                    'or algorithm mismatch)';
                END IF;

                -- 4. Parse payload into JSONB
                BEGIN
                    payload_json := result.payload::jsonb;
                EXCEPTION
                    WHEN OTHERS THEN
                        RAISE EXCEPTION
                        USING ERRCODE = '22023',
                              MESSAGE = format(
                                  'JWT error: payload is not valid JSON (%s)',
                                  result.payload
                              );
                END;

                -- 5. Check expiration (if present)
                IF payload_json ? 'exp' THEN
                    BEGIN
                        exp_epoch := (payload_json->>'exp')::bigint;
                    EXCEPTION
                        WHEN OTHERS THEN
                            RAISE EXCEPTION
                            USING ERRCODE = '22023',
                                  MESSAGE = 'JWT error: exp claim is not '
                                            'a valid number';
                    END;

                    IF exp_epoch < now_epoch THEN
                        RAISE EXCEPTION
                        USING ERRCODE = '22023',
                              MESSAGE = 'JWT error: token has expired';
                    END IF;
                END IF;

                -- 6. Return the payload if all checks pass
                RETURN payload_json;

            END;
            $func$;
        """
        self._run_sql(ddl)