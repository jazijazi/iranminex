import uuid
from datetime import date

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models as gis_models
from django.core.exceptions import ValidationError

from common.models import CustomModel

class Comment(CustomModel):
    sharhlayer = models.ForeignKey(
        'contracts.ShrhLayer',
        verbose_name="لایه شرح خدمات",
        on_delete=models.CASCADE,
        related_name="rcomments",
        blank=False,
        null=False,
        db_index=True,
    )
    writer = models.ForeignKey(
        'accounts.User',
        verbose_name="نویسنده",
        on_delete=models.CASCADE,
        related_name="ruser_comments",
        blank=False,
        null=False,
        db_index=True,
    )
    parent = models.ForeignKey(
        'self',verbose_name="نظر قبلی",
        on_delete=models.CASCADE,
        related_name="replies",
        blank=True,
        null=True,
        db_index=True,
    )
    text = models.TextField(
        verbose_name="متن",
        max_length=500,
        blank=False,
        null=False
    )
    def __str__(self):
        return f"Comment by {self.writer} on {self.sharhlayer}"

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['sharhlayer', '-created_at']),
            models.Index(fields=['writer', '-created_at']),
            models.Index(fields=['parent', '-created_at']),
        ]

    def clean(self):
        """Custom validation"""
        super().clean()
        
        # Prevent self-referencing comments
        if self.parent == self:
            raise ValidationError("نظر نمی‌تواند والد خودش باشد")
        
        # Prevent circular references (comment replying to its own reply)
        if self.parent and self.parent.parent == self:
            raise ValidationError("نمی‌توان به پاسخ خود پاسخ داد")
        
    def save(self, *args, **kwargs):
        """Override save method"""
        self.clean()  # Run validation
        super().save(*args, **kwargs)

    def is_reply(self):
        """Check if this comment is a reply to another comment"""
        return self.parent is not None