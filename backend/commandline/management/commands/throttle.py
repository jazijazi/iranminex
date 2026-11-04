from django.core.management.base import BaseCommand
from django.conf import settings
import redis

class Command(BaseCommand):
    help = "Throttle-related tools: view or delete Redis throttle keys"

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            nargs='?',
            type=str,
            help="Choose 'view_keys' to list or 'delete_keys' to delete throttle keys"
        )

    def handle(self, *args, **options):
        action = options.get('action')

        if action not in ['view_keys', 'delete_keys']:
            self.stdout.write(self.style.WARNING(
                "No valid action provided.\nUsage:\n"
                "  python manage.py throttle view_keys   # List throttle keys\n"
                "  python manage.py throttle delete_keys # Delete throttle keys"
            ))
            return

        # Connect to Redis
        redis_url = settings.CACHES['default']['LOCATION']
        client = redis.StrictRedis.from_url(redis_url)

        if not client.ping():
            self.stderr.write(self.style.ERROR("REDIS NOT CONNECTED!"))
            return
        
        pattern = "m45:django:*:throttle_*"
        keys = list(client.scan_iter(pattern))

        if not keys:
            self.stdout.write(self.style.WARNING("No throttle keys found."))
            return

        if action == 'view_keys':
            self.stdout.write(self.style.SUCCESS(f"Connected to Redis: {redis_url}"))
            self.stdout.write(self.style.SUCCESS(f"Found {len(keys)} throttle keys:\n"))

            for key in keys:
                self.stdout.write(f">>> {key.decode()}")

        elif action == 'delete_keys':
            deleted_count = 0
            for key in keys:
                client.delete(key)
                deleted_count += 1
            self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} throttle keys."))
