from django.core.management.base import BaseCommand

from commandline.publishers.filter_publisher import FilterPublisher


class Command(BaseCommand):

    help = "Publish PostgreSQL tile-filter functions for Martin vector tile server"

    def add_arguments(self, parser):

        parser.add_argument(
            "filter",
            type=str,
            help="Name of the filter function to publish.",
        )

        parser.add_argument(
            "--drop",
            action="store_true",
            default=False,
            help="DROP the function first.",
        )

    def handle(self, *args, **options):

        publisher = FilterPublisher(
            stdout=self.stdout,
            style=self.style,
        )

        publisher.publish(
            filter_name=options["filter"].lower(),
            drop_first=options["drop"],
        )