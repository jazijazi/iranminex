from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = "Publish PostgreSQL views as Martin vector tile layers"

    VIEW_REGISTRY = {
        "ostanviewmini":       "_publish_ostan_layer_mini",
        "shahrestanviewmini":  "_publish_shahrestan_layer_mini",
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "view",
            type=str,
            help=(
                "Name of the view to publish. "
                f"Available: {', '.join(self.VIEW_REGISTRY)}"
            ),
        )
        parser.add_argument(
            "--drop",
            action="store_true",
            default=False,
            help="Drop the view first instead of using CREATE OR REPLACE",
        )
        parser.add_argument(
            "--srid",
            type=int,
            default=3857,
            help="SRID for the geometry column (default: 3857). "
                 "Martin requires a non-zero explicit SRID on views.",
        )

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def handle(self, *args, **options):
        view_key = options["view"].lower()

        if view_key not in self.VIEW_REGISTRY:
            available = ", ".join(self.VIEW_REGISTRY.keys())
            raise CommandError(
                f'Unknown view "{view_key}". Available views: {available}'
            )

        method_name = self.VIEW_REGISTRY[view_key]
        method = getattr(self, method_name)
        method(drop_first=options["drop"], srid=options["srid"])

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

    def _drop_view(self, view_name: str):
        self._run_sql(f"DROP VIEW IF EXISTS {view_name} CASCADE;")
        self.stdout.write(
            self.style.WARNING(f'  ↳ Dropped existing view "{view_name}"')
        )

    def _detect_geometry_type(
        self,
        table_name: str,
        geom_column: str
    ) -> str:
        """
        Reads the geometry type from PostGIS metadata so the CAST in the
        view definition is precise (e.g. MultiPolygon vs Geometry).
        Falls back to 'Geometry' if the column is not yet registered.
        """
        row = self._fetch_one(
            """
            SELECT type
            FROM geometry_columns
            WHERE f_table_name = %s
              AND f_geometry_column = %s
            LIMIT 1
            """,
            [table_name, geom_column],
        )
        return row[0] if row else "Geometry"

    def _create_view(
        self,
        view_name: str,
        db_table: str,
        columns: str,
        drop_first: bool,
    ):
        """
        Generic CREATE [OR REPLACE] VIEW helper shared by all publishers.
        `columns` is a raw SQL column list string, already formatted.
        """
        if drop_first:
            self._drop_view(view_name)
            create_kw = "CREATE VIEW"
        else:
            create_kw = "CREATE OR REPLACE VIEW"

        ddl = f"""
            {create_kw} {view_name} AS
            SELECT
                {columns}
            FROM {db_table};
        """

        try:
            self._run_sql(ddl)
        except Exception as exc:
            raise CommandError(
                f'Failed to create view "{view_name}": {exc}'
            ) from exc

    # ------------------------------------------------------------------
    # View: ostan_layer_mini
    # ------------------------------------------------------------------

    def _publish_ostan_layer_mini(self, drop_first: bool = False, srid: int = 3857):
        """
        CREATE OR REPLACE VIEW ostan_layer_mini AS
        SELECT
            id,
            title AS "عنوان",
            code AS "کد",
            border::geometry(MultiPolygon, 3857) AS border
        FROM <ostan_table>;
        """
        from common.models.districts import Ostan

        db_table  = Ostan._meta.db_table
        view_name = "ostan_layer_mini"
        geom_col  = "border"
        geom_type = self._detect_geometry_type(db_table, geom_col)

        self.stdout.write(
            f'Publishing view "{view_name}" '
            f'from table "{db_table}" '
            f'(geometry: {geom_type}, SRID: {srid}) …'
        )

        columns = f"""id,
                code AS "کد",
                title AS "عنوان",
                {geom_col}::geometry({geom_type}, {srid}) AS {geom_col}"""

        self._create_view(view_name, db_table, columns, drop_first)

        self.stdout.write(self.style.SUCCESS(f'✔  View "{view_name}" published successfully.'))
        self.stdout.write(self.style.SUCCESS(f"   Columns  : id, title, code, {geom_col}"))
        self.stdout.write(self.style.SUCCESS(f"   Geometry : {geom_type} SRID:{srid}"))

    # ------------------------------------------------------------------
    # View: shahrestan_layer_mini
    # ------------------------------------------------------------------

    def _publish_shahrestan_layer_mini(self,drop_first: bool = False,srid: int = 3857,):
        """
        CREATE OR REPLACE VIEW shahrestan_layer_mini AS
        SELECT
            id,
            ostan_id,
            title AS "عنوان",
            code AS "کد",
            border::geometry(MultiPolygon, 3857) AS border
        FROM <shahrestan_table>;
        """
        from common.models.districts import Shahrestan

        db_table = Shahrestan._meta.db_table
        view_name = "shahrestan_layer_mini"

        # Change this if your geometry column has another name
        geom_col = "border"

        geom_type = self._detect_geometry_type(
            db_table,
            geom_col,
        )

        self.stdout.write(
            f'Publishing view "{view_name}" '
            f'from table "{db_table}" '
            f'(geometry: {geom_type}, SRID: {srid}) ...'
        )

        columns = f"""
            id,
            code AS "کد",
            title AS "عنوان",
            ostan_id,
            {geom_col}::geometry({geom_type}, {srid}) AS {geom_col}
        """

        self._create_view(
            view_name=view_name,
            db_table=db_table,
            columns=columns,
            drop_first=drop_first,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'✔ View "{view_name}" published successfully.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"   Columns  : id, code, title, {geom_col}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"   Geometry : {geom_type} SRID:{srid}"
            )
        )