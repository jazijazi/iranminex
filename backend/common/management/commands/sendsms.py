import requests
from django.core.management.base import BaseCommand, CommandError, CommandParser

from common.services.sms_service import send_sms

class Command(BaseCommand):
    help = "Send an SMS to one or more phone numbers."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--phone",
            dest="phones",
            metavar="PHONE",
            nargs="+",
            required=True,
            help="One or more destination phone numbers (e.g. --phone 09121234567 09129876543).",
        )
        parser.add_argument(
            "--text",
            dest="text",
            required=True,
            help="The message body to send.",
        )

    def handle(self, *args, **options) -> None:
        phones: list[str] = options["phones"]
        text: str = options["text"]

        self.stdout.write(
            f"Sending SMS to {len(phones)} number(s): {', '.join(phones)}"
        )

        try:
            send_sms(phones=phones, text=text)
            self.stdout.write(
                self.style.SUCCESS(f"✓ SMS sent successfully to {', '.join(phones)}")
            )
        except (TypeError, ValueError) as exc:
            raise CommandError(f"Invalid input — {exc}") from exc
        except requests.exceptions.RequestException as exc:
            raise CommandError(f"Gateway error — {exc}") from exc