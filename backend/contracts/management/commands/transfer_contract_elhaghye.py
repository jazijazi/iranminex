from django.core.management.base import BaseCommand
from django.db import transaction

from contracts.models.models import Contract, ContractElhaghye


class Command(BaseCommand):
    help = (
        "Transfer existing elhaghye data (elhaghye, mablaghe_elhaghye, tarikh_elhaghye) "
        "from Contract model into the new ContractElhaghye model."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be transferred without actually creating records.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        contracts = Contract.objects.filter(elhaghye=True)
        total = contracts.count()

        if total == 0:
            self.stdout.write(self.style.WARNING("هیچ قراردادی با الحاقیه یافت نشد."))
            return

        self.stdout.write(f"تعداد {total} قرارداد با الحاقیه پیدا شد.")

        created_count = 0
        skipped_count = 0

        with transaction.atomic():
            for contract in contracts:
                # Skip if this contract already has a transferred elhaghye
                # (avoid duplicate creation on repeated command runs)
                already_exists = ContractElhaghye.objects.filter(
                    contract=contract,
                    mablagh=contract.mablaghe_elhaghye,
                    tarikh=contract.tarikh_elhaghye,
                ).exists()

                if already_exists:
                    skipped_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"رد شد (از قبل وجود دارد): {contract.title}"
                        )
                    )
                    continue

                if dry_run:
                    self.stdout.write(
                        f"[DRY RUN] ایجاد می‌شود برای: {contract.title} "
                        f"(مبلغ: {contract.mablaghe_elhaghye}, تاریخ: {contract.tarikh_elhaghye})"
                    )
                    created_count += 1
                    continue

                ContractElhaghye.objects.create(
                    contract=contract,
                    title=f"الحاقیه {contract.title}",
                    mablagh=contract.mablaghe_elhaghye,
                    tarikh=contract.tarikh_elhaghye,
                    description="انتقال شده از فیلدهای قدیمی قرارداد",
                )
                created_count += 1
                self.stdout.write(f"ایجاد شد: {contract.title}")

            if dry_run:
                # rollback nothing was actually created, but just to be explicit
                transaction.set_rollback(True)

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n[DRY RUN] {created_count} رکورد ایجاد می‌شد، {skipped_count} رد می‌شد."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nانتقال کامل شد: {created_count} رکورد ایجاد شد، {skipped_count} رد شد."
                )
            )