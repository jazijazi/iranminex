import uuid
from datetime import timezone

from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models as gis_models
from django.core.exceptions import ValidationError

from common.constants import SCALE_CHOICES
from common.models.models import CustomModel
from common.models.other import Sherkat
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
        ("1", "خدمات مشاوره ایی"),
        ("2", "حفاری"),
        ("3", "ژئوفیزیک"),
        ("4", "چاه پیمایی"),
        ("5", "آزمایشگاه"),
    ]
 
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    # NOTE: the ForeignKey to InitialBorder was removed from here.
    # The relation now lives on InitialBorder.contract
    # (one contract -> many initial borders, reverse accessor: contract.initborders)
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
        },
    )
    moshaver_arshad = models.ForeignKey(
        Sherkat,
        verbose_name="مشاور ارشد",
        on_delete=models.PROTECT,
        related_name="rmoshaverarshadqarardadha",
        blank=True,
        null=True,
    )
    start_date = models.DateField(
        verbose_name="تاریخ شروع",
        blank=True,
        null=True,
    )
    end_date = models.DateField(
        verbose_name="تاریخ پایان",
        blank=True,
        null=True,
    )
    progress = models.FloatField(
        verbose_name="پیشرفت (درصد)",
        default=0,
        validators=[
            MinValueValidator(0, message="پیشرفت نمی‌تواند کمتر از صفر باشد."),
            MaxValueValidator(125, message="پیشرفت نمی‌تواند بیشتر از ۱۲۵ باشد."),
        ],
    )
    is_completed = models.BooleanField(
        verbose_name="خاتمه یافته",
        default=False,
        db_index=True,
    )
    department = models.CharField(
        verbose_name="بخش مربوطه",
        choices=DEPARTMENT_CHOICES,
        max_length=100,
        blank=True,
        null=True,
        error_messages={
            'invalid_choice': (
                'انتخاب نامعتبر است. گزینه‌های معتبر: '
                + ", ".join(f"{k} ({v})" for k, v in DEPARTMENT_CHOICES)
            )
        },
    )
    elhaghye = models.BooleanField(
        verbose_name="الحاقیه دارد",
        default=False,
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
        verbose_name="مبلغ الحاقیه",
        validators=[
            MinValueValidator(0, message="مبلغ الحاقیه نمی‌تواند کمتر از صفر باشد.")
        ],
        blank=True,
        null=True,
    )
    tarikh_elhaghye = models.DateField(
        verbose_name="تاریخ الحاقیه",
        blank=True,
        null=True,
    )
 
    def clean(self):
        """Model validation"""
        super().clean()
        errors = {}

        if self.moshaver_arshad_id:
            if not self.moshaver_arshad.mojaz_moshaver_arshad:
                errors['moshaver_arshad'] = 'این شرکت مجاز به مشاور ارشد بودن نیست.'
            elif not self._state.adding and self.rsherkatha.filter(
                    sherkat_id=self.moshaver_arshad_id).exists():
                errors['moshaver_arshad'] = 'این شرکت در همین قرارداد به‌عنوان شرکت اجرایی ثبت شده است.'

        if self.start_date and self.end_date and self.start_date > self.end_date:
            errors['end_date'] = 'تاریخ پایان نمی‌تواند قبل از تاریخ شروع باشد.'

        if not self._state.adding:
            from initialborders.models.models import ContractInitialBorder
            today = timezone.localdate()
            is_active = not self.is_completed and (self.end_date is None or self.end_date >= today)
            if is_active:
                clash = (
                    ContractInitialBorder.objects
                    .filter(initial_border__contract_links__contract=self)
                    .exclude(contract=self)
                    .filter(contract__is_completed=False)
                    .filter(Q(contract__end_date__isnull=True) | Q(contract__end_date__gte=today))
                    .select_related("initial_border", "contract")
                    .first()
                )
                if clash:
                    errors['is_completed'] = (
                        f"محدوده «{clash.initial_border.title}» هم‌اکنون به قرارداد "
                        f"«{clash.contract.title}» متصل است؛ این قرارداد نمی‌تواند دوباره فعال شود."
                    )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.number or 'بدون شماره'})"
 
    class Meta:
        verbose_name = "قرارداد"
        verbose_name_plural = "قراردادها"
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
