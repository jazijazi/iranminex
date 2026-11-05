import os
from django.db import models
from django.conf import settings
from common.models import CustomModel


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

class SharhbaseAttachmentDomain(CustomModel):
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
        verbose_name = "نوع پیوست بند شرح خدمات"
        verbose_name_plural = "انواع پیوست بند شرح خدمات"

def dynamic_sharhbase_upload_path(instance, filename):
    return f'sharbase/achments/sharhbase_{instance.pk}/sharbaseattachment/{instance.pk}/{filename}'

class SharhbaseAttachment(CustomModel):
    upload_date = models.DateTimeField(
        verbose_name="تاریخ ساخت",
        auto_now_add=True
    )
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="user_sharbaseattachment",
        blank=True,
        null=True
    ) 
    sharhbase = models.ForeignKey(
        'ShrhBase',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='rsharbaseattachment'
    )
    dtyp = models.ForeignKey(
        'SharhbaseAttachmentDomain',
        on_delete=models.SET_NULL,
        related_name="dtyp_sharbaseattachment",
        blank=True,
        null=True
    )
    file = models.FileField(
            verbose_name="فایل",
            blank=False,
            upload_to=dynamic_sharhbase_upload_path,
            max_length=500
        )
    
    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        super().delete(*args, **kwargs)
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

    
    def __str__(self):
        return f'{self.pk} (sharhbase {self.sharhbase.pk})'
    
    class Meta:
        verbose_name = "پیوست بندشرح خدمات"
        verbose_name_plural = "پیوست‌های بندشرح خدمات"   