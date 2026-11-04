from pathlib import Path
import shutil

from django.core.management import BaseCommand, CommandError, call_command


class Command(BaseCommand):
    help = "Create a Django app with jazi-specific structure"

    def add_arguments(self, parser):
        parser.add_argument("name")

    def handle(self, *args, **options):
        app_name = options["name"]
        app_path = Path.cwd() / app_name

        if app_path.exists():
            raise CommandError(
                f"Directory '{app_name}' already exists."
            )

        # Create normal Django app
        call_command("startapp", app_name)

        # Remove default files
        models_file = app_path / "models.py"
        views_file = app_path / "views.py"

        if models_file.exists():
            models_file.unlink()

        if views_file.exists():
            views_file.unlink()

        # Create directories
        directories = [
            "models",
            "services",
            "views",
            "utils",
            "mixin",
            "management",

        ]

        for directory in directories:
            directory_path = app_path / directory
            directory_path.mkdir()
            (directory_path / "__init__.py").touch()

        # Create urls.py
        (app_path / "urls.py").touch() 
        (app_path / "validators.py").touch() 

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created app '{app_name}'."
            )
        )