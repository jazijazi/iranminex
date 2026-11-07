import os
import uuid
from django.db import models

from common.models.models import CustomModel

from django.conf import settings
from django.utils import timezone

def ticket_attachment_path(instance, filename):
    return f"tickets/{instance.number}/{filename}"
def ticket_comment_attachment_path(instance, filename):
    return f"tickets/{instance.ticket.number}/comments/{filename}"


class Ticket(CustomModel):
    class Category(models.TextChoices):
        BUG = "bug" , "گزارش خطا"
        QUESTION = "question" , "سوال"
        SUGGEST = "suggest" , "پیشنهاد"


    class Status(models.TextChoices):
        OPEN = "open", "باز"
        IN_PROGRESS = "in_progress", "در حال انجام"
        ON_HOLD = "on_hold", "متوقف شده"
        RESOLVED = "resolved", "حل شده"
        CLOSED = "closed", "بسته شده"

    class Priority(models.TextChoices):
        LOW = "low", "کم"
        MEDIUM = "medium", "متوسط"
        HIGH = "high", "بالا"
        URGENT = "urgent", "فوری"

    number = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    title = models.CharField(
        max_length=255
    )
    
    body = models.TextField()

    category = models.CharField(
        max_length=20, 
        choices=Category.choices, 
        default=Category.SUGGEST
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets_created",
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )
    @property
    def is_open(self):
        return self.status not in {self.Status.RESOLVED, self.Status.CLOSED}
    
    file = models.FileField(
        verbose_name="فایل",
        blank=True,
        upload_to=ticket_attachment_path,
        max_length=500
    )
    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        self.clean()
        if self.file:
            try:
                if os.path.isfile(self.file.path):
                    os.remove(self.file.path)
                    # Remove empty directories
                    directory = os.path.dirname(self.file.path)
                    if os.path.exists(directory) and not os.listdir(directory):
                        os.rmdir(directory)
            except (OSError, ValueError):
                pass
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "priority"]),
            models.Index(fields=["created_by"]),
        ]

    def __str__(self):
        return f"#{self.number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self._generate_ticket_number()
        if self.status == self.Status.RESOLVED and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)

    def _generate_ticket_number(self):
        return f"TKT-{uuid.uuid4().hex[:8].upper()}"


class TicketComment(CustomModel):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ticket_comments",
    )
    body = models.TextField()

    file = models.FileField(
        verbose_name="فایل",
        blank=True,
        upload_to=ticket_comment_attachment_path,
        max_length=500
    )
    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        self.clean()
        if self.file:
            try:
                if os.path.isfile(self.file.path):
                    os.remove(self.file.path)
                    # Remove empty directories
                    directory = os.path.dirname(self.file.path)
                    if os.path.exists(directory) and not os.listdir(directory):
                        os.rmdir(directory)
            except (OSError, ValueError):
                pass
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.ticket.number}"