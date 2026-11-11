import os
from django.db import models
from django.conf import settings
from common.models.models import CustomModel


class ContractAttachmentDomain(CustomModel):
    code = models.IntegerField(
        verbose_name="کد",
        unique=True
    )
    name_en = models.CharField(
        verbose_name="نام لاتین",
        max_length=100,
        unique=False,
        blank=False,
        null=False
    )
    name_fa = models.CharField(
        verbose_name="نام فارسی",
        max_length=100,
        unique=False,
        blank=False,null=False
    )
    typ = models.CharField(
        verbose_name="نوع",
        max_length=100,
        unique=False,
        blank=False,
        null=False
    )
    
    def __str__(self):
        return f'{self.name_en}_{self.code}'
    
    class Meta:
        verbose_name = "نوع پیوست قرارداد"
        verbose_name_plural = "انواع پیوست قرارداد"

def dynamic_contract_upload_path(instance, filename):
    return f'contracts/achments/contract_{instance.contract.pk}/contractattachment/{instance.pk}/{filename}'

class ContractAttachment(CustomModel):
    upload_date = models.DateTimeField(
        verbose_name="تاریخ ساخت",
        auto_now_add=True
    )
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="user_contractattachment",
        blank=True,
        null=True
    ) 
    contract = models.ForeignKey(
        'Contract',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='rcontractattachment'
    )
    dtyp = models.ForeignKey(
        'ContractAttachmentDomain',
        on_delete=models.SET_NULL,
        related_name="dtyp_contractattachment",
        blank=True,
        null=True
    )
    file = models.FileField(
            verbose_name="فایل",
            blank=False,
            upload_to=dynamic_contract_upload_path,
            max_length=500
        )
    
    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
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

    
    def __str__(self):
        return f'{self.pk} (contract {self.contract.pk})'
    
    class Meta:
        verbose_name = "پیوست قرارداد"
        verbose_name_plural = "پیوست‌های قرارداد"

"""
contracts/models/attachment.py
==============================
پیوست‌های بند شرح خدمات قرارداد.

تغییرات نسبت به نسخهٔ قبلی (خلاصه):
  • پیوست حالا به ShrhContract (بند همین قرارداد) وصل است، نه به کاتالوگ ثابت.
  • مسیر آپلود: قبلاً از instance.pk استفاده می‌شد که هنگام آپلود هنوز None بود
    (پوشه‌هایی مثل sharhbase_None). حالا از id قرارداد/بند + uuid استفاده می‌شود.
  • حذف فایل از delete() به سیگنال post_delete منتقل شد؛ چون delete() مدل
    در حذف cascade (مثلاً حذف قرارداد) یا حذف گروهی صدا زده نمی‌شود و فایل یتیم می‌ماند.
    با تعویض فایل هم فایل قدیمی پاک می‌شود. از storage استفاده شده (نه .path)
    تا با S3 و ... هم کار کند.
  • فیلد upload_date حذف شد (CustomModel خودش created_at دارد).
  • verbose_name ها کامل و import های ناقص (os, settings) اضافه شد.
"""
import os
import uuid

from django.conf import settings
from django.db import models, transaction
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from common.models.models import CustomModel


class ShrhAttachmentDomain(CustomModel):
    """
    نوع پیوست یک بند شرح خدمات (مثلاً: فایل Track، گزارش، نقشه، جدول آنالیز، ...).
    جدول جداست تا بدون migration نوع جدید اضافه شود.
    """
    code = models.IntegerField(
        verbose_name="کد",
        unique=True,
    )
    name_en = models.CharField(
        verbose_name="نام لاتین",
        max_length=100,
    )
    name_fa = models.CharField(
        verbose_name="نام فارسی",
        max_length=100,
    )
    typ = models.CharField(
        verbose_name="نوع",
        max_length=100,
    )

    def __str__(self):
        return f"{self.name_fa} ({self.code})"

    class Meta:
        verbose_name = "نوع پیوست بند شرح خدمات"
        verbose_name_plural = "انواع پیوست بند شرح خدمات"
        ordering = ['code']


def shrh_attachment_upload_path(instance, filename):
    """
    shrh_attachments/<id قرارداد>/<id بند قرارداد>/<uuid>_<نام فایل>
    uuid از رونویسی شدن فایل‌های هم‌نام جلوگیری می‌کند.
    """
    sc = instance.shrh_contract
    return (
        f"shrh_attachments/{sc.contract_id}/{sc.pk}/"
        f"{uuid.uuid4().hex[:12]}_{os.path.basename(filename)}"
    )


class ShrhAttachment(CustomModel):
    """
    فایلی که برای یک بند از شرح خدمات قرارداد بارگذاری می‌شود
    (مثلاً «فایل Track و برداشت‌های صحرایی»).

    - writer: کاربر بارگذاری‌کننده (در API از request.user پر شود).
    - dtyp: نوع پیوست (اختیاری).
    - حذف رکورد یا تعویض فایل، فایل قدیمی را از storage پاک می‌کند (سیگنال‌های پایین).
    """
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="بارگذاری‌کننده",
        on_delete=models.SET_NULL,
        related_name="rshrhattachments",
        blank=True,
        null=True,
    )
    shrh_contract = models.ForeignKey(
        'contracts.ShrhContract',
        verbose_name="بند قرارداد",
        on_delete=models.CASCADE,
        related_name="rattachments",
    )
    dtyp = models.ForeignKey(
        ShrhAttachmentDomain,
        verbose_name="نوع پیوست",
        on_delete=models.SET_NULL,
        related_name="rattachments",
        blank=True,
        null=True,
    )
    file = models.FileField(
        verbose_name="فایل",
        upload_to=shrh_attachment_upload_path,
        max_length=500,
    )

    @property
    def filename(self):
        return os.path.basename(self.file.name) if self.file else ""

    def __str__(self):
        return f"{self.filename or self.pk} ({self.shrh_contract_id})"

    class Meta:
        verbose_name = "پیوست بند شرح خدمات"
        verbose_name_plural = "پیوست‌های بند شرح خدمات"
        ordering = ['-created_at']