import uuid
from datetime import date

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models as gis_models
from django.core.exceptions import ValidationError

from common.constants import SCALE_CHOICES
from common.models import CustomModel
from common.models import Province , Company
from initialborders.models.models import InitialBorder


class ContractDomin(CustomModel):
    title = models.CharField(max_length=100, unique=True)
    code = models.IntegerField(unique=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "نوع قرادادها"
        verbose_name_plural = "انواع قرادادها"

class Contract(CustomModel):

    DEPARTMENT_CHOICES = [
        ("1" , "خدمات مشاوره ایی"),
        ("2" , "حفاری"),
        ("3" , "ژئوفیزیک"),
        ("4" , "چاه پیمایی"),
        ("5" , "آزمایشگاه"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    initborder = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="rinitcontractborders",
        blank=False,
        null=False
    )
    title = models.CharField(
        verbose_name="عنوان قرارداد",
        max_length=250,
        unique=True,
        error_messages={
            'unique': "قراردادی با این عنوان هم‌اکنون وجود دارد",
        },
    )
    dtyp = models.ForeignKey(
        ContractDomin,
        verbose_name="نوع قرارداد",
        on_delete=models.SET_NULL,
        related_name="rdtypcontracts",
        blank=True, 
        null=True,
    )
    number = models.CharField(
        verbose_name="شماره قرارداد",
        max_length=100,
        blank=True, 
        null=True,
        unique=True,
        error_messages={
            'unique': "شماره قرارداد تکراری است"
        }
    )
    company = models.ManyToManyField(
        Company,
        verbose_name="شرکت",
        related_name="rcompanycontracts",
        blank=True
    )    
    start_date = models.DateField(
        verbose_name="تاریخ شروع",
        blank=True,
        null=True
    )
    end_date = models.DateField(
        verbose_name="تاریخ پایان",
        blank=True,
        null=True
    )
    progress = models.FloatField(
        verbose_name="پیشرفت (درصد)",
        default=0,
        validators=[
            MinValueValidator(0, message="پیشرفت نمی‌تواند کمتر از صفر باشد."),
            MaxValueValidator(125, message="پیشرفت نمی‌تواند بیشتر از صد باشد.")
        ],
    )
    is_completed = models.BooleanField(
        verbose_name="خاتمه یافته",
        default=False,
        db_index=True
    )
    department = models.CharField(
        verbose_name="بخش مربوطه",
        default="-",
        choices=DEPARTMENT_CHOICES,
        max_length=100,
        unique=False,
        blank=True,
        null=True,
        error_messages={
            'invalid_choice': f'انتخاب نامعتبر است. گزینه‌های معتبر: {", ".join([f"{choice[0]} ({choice[1]})" for choice in DEPARTMENT_CHOICES])}'
        }
    )
    # sherkatejraei = models.ManyToManyField('SherkatEjraei', related_name="rgharardads", blank=True,)
    # additional fields
    elhaghye = models.BooleanField(
        verbose_name="الحاقیه دارد",
        default=False,
        blank=False,
        null=False
    )
    mablagh = models.BigIntegerField(
        verbose_name="مبلغ قرارداد",
        validators=[
            MinValueValidator(0, message="مبلغ قرارداد نمی‌تواند کمتر از صفر باشد.")
        ],
        null=True,
        blank=True,
    )
    mablaghe_elhaghye = models.BigIntegerField(
        verbose_name="مبلغ الحاقیه",validators=[
            MinValueValidator(0, message="مبلغ الحاقیه نمی‌تواند کمتر از صفر باشد.")
        ],
        blank=True,
        null=True
    )
    tarikh_elhaghye = models.DateField(
        verbose_name="تاریخ الحاقیه",
        blank=True,
        null=True,
    )
    initborder = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="rinitcontractborders",
        blank=False,
        null=False
    )

    def clean(self):
        """Model validation"""
        super().clean()
        
        # Validate date range
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError({
                    'end_date': 'تاریخ پایان نمی‌تواند قبل از تاریخ شروع باشد.',
                })

    def __str__(self):
        return f"{self.title} ({self.number or 'بدون شماره'})"

    class Meta:
        verbose_name = "قراداد"
        verbose_name_plural = "قرادادها"
        ordering = ['-created_at']

class ContractElhaghye(CustomModel):

    contract = models.ForeignKey(
        Contract,
        verbose_name="قرارداد",
        on_delete=models.CASCADE,
        related_name="relhaghyeha",
    )
    title = models.CharField(
        verbose_name="عنوان الحاقیه",
        max_length=250,
        blank=True,
        null=True,
    )
    mablagh = models.BigIntegerField(
        verbose_name="مبلغ الحاقیه",
        validators=[
            MinValueValidator(0, message="مبلغ الحاقیه نمی‌تواند کمتر از صفر باشد.")
        ],
        blank=True,
        null=True,
    )
    tarikh = models.DateField(
        verbose_name="تاریخ الحاقیه",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="توضیحات",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"الحاقیه {self.title or '-'} - {self.contract.title}"

    class Meta:
        verbose_name = "الحاقیه قرارداد"
        verbose_name_plural = "الحاقیه‌های قرارداد"
        ordering = ['-tarikh']

from .SharhKhadamats import *
from .comments import *
from .attachment import *
