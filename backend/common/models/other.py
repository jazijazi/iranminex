from django.db import models


from common.models.models import CustomModel


class NoeKhadamat(CustomModel):
    """نوع خدمات شرکت‌ها: اکتشاف، حفاری، ژئوفیزیک، چاه‌پیمایی، آزمایشگاه، ..."""

    title = models.CharField(
        verbose_name="عنوان",
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "نوع خدمات"
        verbose_name_plural = "انواع خدمات"

class Sherkat(CustomModel):
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
    noe_khadamat = models.ManyToManyField(
        NoeKhadamat,
        verbose_name="نوع خدمات",
        related_name="rSherkatha",
        blank=True,
    )
    mojaz_moshaver_arshad = models.BooleanField(
        verbose_name="مجاز به مشاور ارشد بودن",
        default=True,
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

    
