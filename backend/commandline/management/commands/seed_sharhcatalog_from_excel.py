import re
from pathlib import Path

import openpyxl

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from contracts.models.SharhKhadamats import Faz, Vahed, ShrhCatalog

class Command(BaseCommand):
    help = "Seed Faz and ShrhCatalog from an Excel file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default=str(settings.BASE_DIR / "sharcatalog.xlsx"),
            help="Path to the Excel file.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate and preview without saving changes.",
        )

    @staticmethod
    def normalize(value):
        if value is None:
            return ""

        value = str(value)
        value = value.replace("ي", "ی").replace("ك", "ک")
        value = value.replace("\u200c", " ")
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    @staticmethod
    def is_phase_row(cell, title):
        color = cell.fill.fgColor

        return (
            title.startswith("فاز ")
            and color.type == "rgb"
            and color.rgb in ("FFFFC000", "00FFC000")
        )

    @staticmethod
    def is_group_row(cell, unit):
        color = cell.fill.fgColor

        return (
            not unit
            and cell.font.bold
            and color.type == "theme"
            and color.theme == 4
        )

    def handle(self, *args, **options):
        excel_path = Path(options["file"])
        dry_run = options["dry_run"]

        if not excel_path.exists():
            raise CommandError(f"Excel file not found: {excel_path}")

        workbook = openpyxl.load_workbook(
            excel_path,
            data_only=True,
        )

        worksheet = workbook.active

        # Obtain the Vahed model through the ForeignKey.
        Vahed = ShrhCatalog._meta.get_field("vahed").remote_field.model

        # Match existing units using their string representation.
        vahed_map = {
            self.normalize(obj.title): obj
            for obj in Vahed.objects.all()
        }

        faz = None
        parent = None

        faz_count = 0
        group_count = 0
        activity_count = 0
        missing_units = []

        with transaction.atomic():

            for row in range(3, worksheet.max_row + 1):

                code = worksheet.cell(row, 1).value
                title = self.normalize(worksheet.cell(row, 2).value)
                description = self.normalize(
                    worksheet.cell(row, 4).value
                )
                unit_title = self.normalize(
                    worksheet.cell(row, 5).value
                )

                if code is None or not title:
                    continue

                code = int(code)

                title_cell = worksheet.cell(row, 2)

                # Skip the project title.
                if code == 1:
                    continue

                # Phase row.
                if self.is_phase_row(title_cell, title):

                    if not dry_run:
                        faz, created = Faz.objects.update_or_create(
                            title=title,
                            defaults={
                                "order": faz_count,
                            },
                        )

                    else:
                        faz = title

                    faz_count += 1
                    parent = None

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"PHASE: {title}"
                        )
                    )

                    continue

                if faz is None:
                    raise CommandError(
                        f"Row {row}: Activity found before any phase."
                    )

                # Resolve unit.
                vahed = None

                if unit_title:
                    vahed = vahed_map.get(unit_title)

                    if vahed is None:
                        if not dry_run:
                            vahed, created = Vahed.objects.get_or_create(
                                title=unit_title
                            )
                            vahed_map[unit_title] = vahed

                            if created:
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f"  NEW UNIT: {unit_title}"
                                    )
                                )
                        else:
                            self.stdout.write(
                                f"  NEW UNIT (DRY RUN): {unit_title}"
                            )

                if self.is_group_row(title_cell, unit_title):

                    # Group row.
                    if not dry_run:
                        obj, created = ShrhCatalog.objects.update_or_create(
                            code=code,
                            defaults={
                                "faz": faz,
                                "parent": None,
                                "is_group": True,
                                "title": title,
                                "vahed": None,
                                "description": description,
                                "order": code,
                            },
                        )

                        parent = obj

                    else:
                        parent = title

                    group_count += 1

                    self.stdout.write(
                        f"  GROUP: {code} - {title}"
                    )

                else:

                    # Activity row.
                    if unit_title and vahed is None:
                        continue

                    if not dry_run:
                        ShrhCatalog.objects.update_or_create(
                            code=code,
                            defaults={
                                "faz": faz,
                                "parent": parent,
                                "is_group": False,
                                "title": title,
                                "vahed": vahed,
                                "description": description,
                                "order": code,
                            },
                        )

                    activity_count += 1

                    self.stdout.write(
                        f"    ACTIVITY: {code} - {title}"
                    )

            if missing_units:
                raise CommandError(
                    "Some units were not found in Vahed:\n"
                    + "\n".join(missing_units)
                    + "\nNo database changes were committed."
                )

            if dry_run:
                # Roll back the transaction even if future changes
                # accidentally introduce database writes.
                transaction.set_rollback(True)

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Seeding completed successfully."
            )
        )

        self.stdout.write(f"Phases: {faz_count}")
        self.stdout.write(f"Groups: {group_count}")
        self.stdout.write(f"Activities: {activity_count}")

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN: No changes saved.")
            )