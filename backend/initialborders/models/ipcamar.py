from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from common.models import CustomModel
from initialborders.models.models import InitialBorder

class IpcAmarEkteshaf(CustomModel):

    initialborder = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="ripcamarekteshaf",
        blank=False,
        null=False
    )
    sal = models.IntegerField(
        verbose_name="سال",
        null=False,
        blank=False
    )
    doure = models.IntegerField(
        verbose_name="دوره" ,
        validators=[
            MinValueValidator(1, message="دوره نمی‌تواند کمتر از 1 باشد."),
            MaxValueValidator(12, message="دوره نمی‌تواند بیشتر از 12 باشد.")
        ],
        null=False,
        blank=False
    )
    faz = models.CharField(
        #Choice ??
        verbose_name="فاز",
        max_length=128,
        blank=False,
        null=False,
    )
    shakhes = models.CharField(
        #Choice ??
        verbose_name="شاخص",
        max_length=128,
        blank=False,
        null=False,
    )
    vahed = models.CharField(
        #Choice ??
        verbose_name="واحد",
        max_length=128,
        blank=False,
        null=False,
    )
    meghdar = models.FloatField(
        blank=True,
        null=True
    )
    descriptions = models.CharField(
        verbose_name="توضیحات",
        max_length=128,
        blank=True,
        null=True,
    )

    def clean(self):
        super().clean()

    def __str__(self):
        return f"آمار اکتشاف تهیه تولید {self.initialborder.title}"
    
    class Meta:
        verbose_name = "آمار اکتشاف تهیه تولید"
        verbose_name_plural = "آمارهای اکتشاف تهیه تولید"

class IpcBarnamehEkteshaf(CustomModel):

    sal = models.IntegerField(
        verbose_name="سال",
        null=False,
        blank=False
    )
    faz = models.CharField(
        #Choice ??
        verbose_name="فاز",
        max_length=128,
        blank=False,
        null=False,
    )
    shakhes = models.CharField(
        #Choice ??
        verbose_name="شاخص",
        max_length=128,
        blank=False,
        null=False,
    )
    vahed = models.CharField(
        #Choice ??
        verbose_name="واحد",
        max_length=128,
        blank=False,
        null=False,
    )
    meghdar = models.FloatField(
        blank=True,
        null=True
    )
    descriptions = models.CharField(
        verbose_name="توضیحات",
        max_length=128,
        blank=True,
        null=True,
    )

    def clean(self):
        super().clean()

    def __str__(self):
        return f"برنامه عملکرد اکتشاف تهیه تولید {self.sal}"
    
    class Meta:
        verbose_name = "برنامه عملکرد اکتشاف تهیه تولید"
        verbose_name_plural = "برنامه‌های عملکرد اکتشاف تهیه تولید"
