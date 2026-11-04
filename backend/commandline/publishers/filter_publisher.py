from pathlib import Path

from django.core.management.base import CommandError
from django.db import connection


class FilterPublisher:

    FILTERS = {
        "common_pelak_by_user_access": {
            "sql_file": "common_pelak_by_user_access.sql",
            "signature": "public.common_pelak_by_user_access(integer, integer, integer, json)",
        },
        "pelak_tile_filter": {
            "sql_file": "pelak_tile_filter.sql",
            "signature": "public.pelak_tile_filter(integer, integer, integer, json)",
        },
        "pelak_user_filter": {
            "sql_file": "pelak_user_filter.sql",
            "signature": "public.pelak_user_filter(integer, integer, integer, json)",
        },
        "contract_pelak_border_filter": {
            "sql_file": "contract_pelak_border_filter.sql",
            "signature": "public.contract_pelak_border_filter(integer, integer, integer, json)",
        },
        "user_pelak_by_shahrestanid": {
            "sql_file": "user_pelak_by_shahrestanid.sql",
            "signature": "public.user_pelak_by_shahrestanid(integer, integer, integer, json)",
        },
        "karbargetwopelak_filterby_contractid": {
            "sql_file": "karbargetwopelak_filterby_contractid.sql",
            "signature": "public.karbargetwopelak_filterby_contractid(integer, integer, integer, json)",
        },
        "sakhtarkoli_by_pelak":{
            "sql_file":"sakhtarkoli_by_pelak.sql",
            "signature":"public.sakhtarkoli_by_pelak(integer, integer, integer, json)",
        },

    }

    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style

    def load_sql(self, filename):
        """
        Read SQL file from commandline/sql/filters/
        """

        sql_dir = Path(__file__).resolve().parent.parent / "sql" / "filters"
        sql_file = sql_dir / filename

        if not sql_file.exists():
            raise CommandError(
                f"SQL file not found: {sql_file}"
            )

        return sql_file.read_text(encoding="utf-8")

    def drop_function(self, signature):
        """
        Drop an existing PostgreSQL function.
        """

        with connection.cursor() as cursor:
            cursor.execute(
                f"DROP FUNCTION IF EXISTS {signature} CASCADE;"
            )

        self.stdout.write(
            self.style.WARNING(
                f'  ↳ Dropped existing function "{signature}"'
            )
        )

    def execute(self, sql):
        """
        Execute SQL against Django's database.
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)

        except Exception as exc:
            raise CommandError(
                f"Failed to execute SQL: {exc}"
            ) from exc

    def report_success(self, filter_name):
        """
        Print success message.
        """

        self.stdout.write(
            self.style.SUCCESS(
                f'✔ Function "{filter_name}" published successfully.'
            )
        )

    def publish(self, filter_name, drop_first=False):
        """
        Complete publishing process.
        """

        if filter_name not in self.FILTERS:
            available = ", ".join(self.FILTERS)
            raise CommandError(
                f'Unknown filter "{filter_name}". Available: {available}'
            )

        config = self.FILTERS[filter_name]

        self.stdout.write(
            f'Publishing filter function "{filter_name}" …'
        )

        if drop_first:
            self.drop_function(config["signature"])

        sql = self.load_sql(config["sql_file"])

        self.execute(sql)

        self.report_success(filter_name)