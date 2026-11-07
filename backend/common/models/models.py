import logging
from typing import Optional
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from common.utils.ipget import get_client_ip
from common.middleware import get_current_request


class CustomModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    created_ip = models.GenericIPAddressField(
        protocol='both',
        null=True,
        blank=True,
        editable=False,
        verbose_name="IP ایجاد",
    )
    updated_ip = models.GenericIPAddressField(
        protocol='both',
        null=True,
        blank=True,
        editable=False,
        verbose_name="IP بروزرسانی",
    )

    def save(self, *args, **kwargs):
        ip = self._resolve_ip()
        is_new = self._state.adding

        if is_new and self.created_ip is None:
            self.created_ip = ip

        self.updated_ip = ip

        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            update_fields = set(update_fields)
            update_fields.add("updated_ip")

            if is_new:
                update_fields.add("created_ip")

            kwargs["update_fields"] = list(update_fields)

        return super().save(*args, **kwargs)

    def _resolve_ip(self) -> Optional[str]:
        """
        Safely resolves IP from current request thread-local.
        Returns None in all failure cases — never raises.
        """
        try:
            request = get_current_request()

            if request is None:
                # Normal: management commands, celery, tests, shell
                return None

            ip = get_client_ip(request)

            # '0.0.0.0' is our failure sentinel — treat as no IP
            if not ip or ip == '0.0.0.0':
                return None

            return ip

        except Exception as e:
            logging.warning(f"[CustomModel] IP resolution failed: {e}")
            return None

    class Meta:
        abstract = True
        ordering = ["-updated_at"]

class DeletionLog(models.Model):
    """
    One row per deleted object, of ANY model. Written automatically by the
    pre_delete signal in signals.py - you never create these by hand and
    you never need to touch your existing models to make this work.
    """

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="مدل",
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    deleted_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="زمان حذف"
    )
    ip_address = models.GenericIPAddressField(
        protocol='both',
        null=True,
        blank=True,
        editable=False,
        verbose_name="IP حذف",
    )
    object_id = models.BigIntegerField(verbose_name="شناسه رکورد حذف‌شده")
    data = models.JSONField(verbose_name="داده‌های رکورد در لحظه حذف")

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"])]
        ordering = ["-deleted_at"]
        verbose_name = "لاگ حذف"
        verbose_name_plural = "لاگ حذف‌ها"

    def __str__(self):
        return f"{self.content_type} #{self.object_id} @ {self.deleted_at}"


