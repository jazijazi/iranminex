from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from logs.models import Logs  # replace with your app name

class Command(BaseCommand):
    help = 'Delete Logs older than specified number of days'

    def add_arguments(self, parser):
        parser.add_argument(
            'days',
            nargs='?',
            type=int,
            default=None,
            help='Delete logs older than this number of days (positional)'
        )
        parser.add_argument(
            '--days',
            dest='days_opt',  # <-- different name to avoid conflict
            type=int,
            help='Delete logs older than this number of days (optional)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show how many logs would be deleted without deleting them'
        )

    def handle(self, *args, **kwargs):
        # Use positional if given, otherwise optional
        days = kwargs.get('days') or kwargs.get('days_opt')
        if days is None or days <= 0:
            self.stdout.write(self.style.ERROR("Please provide a positive number of days"))
            return

        cutoff_date = timezone.now() - timedelta(days=days)
        old_logs = Logs.objects.filter(tarikh__lt=cutoff_date)
        count = old_logs.count()

        if kwargs.get('dry_run'):
            self.stdout.write(self.style.WARNING(
                f"[Dry Run] {count} log(s) would be deleted (older than {days} days)"
            ))
        else:
            old_logs.delete()
            self.stdout.write(self.style.SUCCESS(
                f"Deleted {count} log(s) older than {days} days"
            ))