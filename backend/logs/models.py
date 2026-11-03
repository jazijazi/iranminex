from django.db import models


LEVEL_OPTIONS = [
    ("DEBUG", "DEBUG"),
    ("INFO", "INFO"),
    ("WARNING", "WARNING"),
    ("ERROR", "ERROR"),
    ("CRITICAL", "CRITICAL"),
]

METHOD_OPTIONS = [
    ("GET", "GET"),
    ("POST", "POST"),
    ("PUT", "PUT"),
    ("PATCH", "PATCH"),
    ("DELETE", "DELETE"),
    ("OTHER", "OTHER"),
]

class Logs(models.Model):
    username = models.CharField(
        max_length=100,
        unique=False,
        blank=True,
        null=True
    )
    writer = models.CharField(
        max_length=100,
        unique=False,
        blank=True,
        null=True
    )
    tarikh = models.DateTimeField(
        auto_created=True,
        blank=True,
        null=True
    )
    level = models.CharField(
        max_length=25,
        choices=LEVEL_OPTIONS
    )
    ip = models.GenericIPAddressField(
        blank=True,
        null=True
    )
    method = models.CharField(
        max_length=25,
        choices=METHOD_OPTIONS
    )
    route = models.CharField(
        max_length=100,
        unique=False,
        blank=True,
        null=True
    )
    massage = models.TextField(
        max_length=2000,
        unique=False,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.level} - {self.writer}'
    
    class Meta:
        verbose_name = "لاگ"
        verbose_name_plural = "لیست لاگ ها"    