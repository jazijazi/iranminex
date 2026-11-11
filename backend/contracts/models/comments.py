"""
contracts/models/comments.py
============================
نظرات روی لایه‌های شرح خدمات (با پاسخ‌های تو در تو).

تغییرات نسبت به نسخهٔ قبلی (خلاصه):
  • نام مدل و فیلد با بقیه یکدست شد: Comment → ShrhLayerComment ، sharhlayer → shrh_layer
    (related_name روی لایه همان rcomments ماند).
  • 'accounts.User' → settings.AUTH_USER_MODEL.
  • writer: CASCADE → SET_NULL؛ با حذف کاربر، تاریخچهٔ گفتگوی لایه پاک نشود.
  • db_index=True از FK ها برداشته شد (FK خودش index دارد) و index های ترکیبی ماند.
  • clean() قبلی عملاً کاری نمی‌کرد: `self.parent.parent == self` هرگز درست نمی‌شود
    چون نظر جدید نمی‌تواند والدِ والدِ خودش باشد. به‌جایش این قواعد آمد:
      ۱) والد باید برای همان لایه باشد،
      ۲) فقط یک سطح پاسخ مجاز است (به پاسخ نمی‌شود پاسخ داد)،
      ۳) متن خالی/فقط‌فاصله مجاز نیست.
    اگر پاسخ تو در تو (چندسطحی) می‌خواهید، قاعدهٔ ۲ را بردارید.
  • save() به‌جای clean() فقط، full_clean() را اجرا می‌کند (مثل بقیهٔ مدل‌ها).
  • max_length روی TextField فقط در فرم اعمال می‌شود؛ MaxLengthValidator اضافه شد.
  • is_reply یک property شد.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models

from common.models.models import CustomModel


class ShrhLayerComment(CustomModel):
    shrh_layer = models.ForeignKey(
        'contracts.ShrhLayer',
        verbose_name="لایه شرح خدمات",
        on_delete=models.CASCADE,
        related_name="rcomments",
    )
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="نویسنده",
        on_delete=models.SET_NULL,
        related_name="rshrhcomments",
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        'self',
        verbose_name="نظر قبلی",
        on_delete=models.CASCADE,
        related_name="replies",
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name="متن",
        max_length=500,
        validators=[MaxLengthValidator(500, message="متن نظر نمی‌تواند بیشتر از ۵۰۰ کاراکتر باشد.")],
    )

    @property
    def is_reply(self):
        return self.parent_id is not None

    def clean(self):
        super().clean()
        errors = {}

        if self.text is not None and not self.text.strip():
            errors['text'] = "متن نظر نمی‌تواند خالی باشد."

        if self.parent_id:
            if self.pk and self.parent_id == self.pk:
                errors['parent'] = "نظر نمی‌تواند والد خودش باشد."
            elif self.parent.shrh_layer_id != self.shrh_layer_id:
                errors['parent'] = "نظر قبلی باید مربوط به همین لایه باشد."
            elif self.parent.parent_id:
                errors['parent'] = "فقط می‌توان به نظر اصلی پاسخ داد، نه به یک پاسخ."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"نظر {self.writer or 'کاربر حذف‌شده'} روی {self.shrh_layer_id}"

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['shrh_layer', '-created_at']),
            models.Index(fields=['writer', '-created_at']),
            models.Index(fields=['parent', '-created_at']),
        ]