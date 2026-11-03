from django.db import models
from django.contrib.gis.db import models as gis_models

class CustomModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        abstract = True

class Province(models.Model):
    name_fa = models.CharField(
        verbose_name="نام",
        unique=True,
        blank=False,
        null=False,
    )
    cnter_name_fa = models.CharField(
        verbose_name="نام مرکز",
        unique=True,
        blank=False,
        null=False,
    )
    code = models.PositiveIntegerField(
        verbose_name="کد",
        unique=True,
        blank=False,
        null=False,
    )
    border = gis_models.MultiPolygonField(
        srid=4326,
        blank=False,
        null=False
    )

    def __str__(self):
        return f"province {self.name_fa} ({self.code})"
    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان ها"

class County(models.Model):
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        related_name="rprovince",
        blank=True,
        null=True,
    )
    name_fa = models.CharField(
        verbose_name="نام",
        unique=True,
        blank=False,
        null=False,
    )
    code = models.PositiveIntegerField(
        verbose_name="کد",
        unique=True,
        blank=False,
        null=False,
    )
    border = gis_models.MultiPolygonField(
        srid=4326,
        blank=False,
        null=False
    )

    def __str__(self):
        return f"County {self.name_fa} ({self.code})"
    class Meta:
        verbose_name = "شهرستان"
        verbose_name_plural = "شهرستان ها"



class Company(models.Model):
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

    
