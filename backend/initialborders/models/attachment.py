import os
from django.db import models

from django.conf import settings

def dynamic_upload_path(instance, filename):
    return f'initialborder/achments/initialborder_{instance.rinitialborder.id}/{filename}'


class InitialBorderAttachment(models.Model):
    upload_date = models.DateTimeField(verbose_name="تاریخ ساخت پیوست",auto_now_add=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="user_initialborderachment", blank=True, null=True) 
    writed_date = models.DateTimeField(verbose_name="تاریخ نوشتن پیوست",auto_now_add=False,blank=True,null=True)
    rinitialborder = models.ForeignKey('InitialBorder', on_delete=models.CASCADE, blank=False, null=False, related_name='rinitialborderachment')
    dtyp_attach = models.ForeignKey('InitialBorderAttachmentDomain', on_delete=models.SET_NULL, related_name="dtyp_initialborderattachment", blank=True, null=True)
    file = models.FileField(
            verbose_name="فایل",
            blank=False,
            upload_to=dynamic_upload_path,
        )
    
    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)

    
    def __str__(self):
        return f"{self.rinitialborder.title}_{self.dtyp_attach.name if self.dtyp_attach and self.dtyp_attach.name else '-'}_{self.file.name}"
    
    class Meta:
        verbose_name = "اتچمنت محدوده های اولیه"
        verbose_name_plural = "اتچمنت های محدوده های اولیه"


class InitialBorderAttachmentDomain(models.Model):
    code = models.IntegerField(verbose_name="کد پیوست" , unique=True , error_messages={'unique': "کد پیوست باید یکتا باشد.",})
    name = models.CharField(verbose_name="عنوان نوع پیوست",max_length=100, unique=False, blank=False, null=False)
    category = models.CharField(verbose_name="دسته بندی",max_length=100, unique=False, blank=False, null=False)
    dinitialborder = models.ForeignKey('InitialBorderDomin', on_delete=models.SET_NULL, related_name="rinitialborderattachmentdomin", blank=True, null=True)

    def __str__(self):
        return f'{self.name}_({self.dinitialborder.title})'
    
    class Meta:
        verbose_name = "نوع پیوست محدوده اولیه"
        verbose_name_plural = "انواع پیوست محدوده اولیه"