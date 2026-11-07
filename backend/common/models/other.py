from django.db import models


from common.models.models import CustomModel

class Company(CustomModel):
    name = models.CharField(
        verbose_name="نام شرکت",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        error_messages={
            'unique': "شرکتی با این نام قبلاً ثبت شده است."
        }
    )
    code = models.CharField(
        verbose_name="کد شناسایی شرکت" , 
        max_length=100 ,
         blank=True,
         null=True, 
         unique=False
    )
    typ = models.CharField(
        verbose_name="نوع شرکت",
        max_length=100, 
        blank=True,
        null=True, 
        unique=False
    )
    service_typ = models.CharField(
        verbose_name="نوع خدمات",
        max_length=100, 
        blank=True,
        null=True, 
        unique=False
    )
    callnumber = models.CharField(
        verbose_name="شماره تماس",
        max_length=100, 
        blank=True,
        null=True, 
        unique=False
    )
    address = models.CharField(
        verbose_name="آدرس",
        max_length=255, 
        blank=True,
        null=True, 
        unique=False
    )
    comment = models.CharField(
        verbose_name="توضیحات",
        max_length=255, 
        blank=True,
        null=True, 
        unique=False
    )

    class Meta:
        verbose_name = "لیست شرکت"
        verbose_name_plural = "لیست شرکت ها"
    
    def __str__(self):
        return f"{self.name}"

    
