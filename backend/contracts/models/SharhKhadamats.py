from django.db import models
from django.core.validators import MinValueValidator , MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings

from common.models import CustomModel
from common.constants import SCALE_CHOICES
from contracts.models.models import Contract
from layers.models.models import LayersNames


class ShrhBase(CustomModel):
    """
    Service description items for contracts
    هر رکورد در این جدول یک بند از شرح خدمات قرارداد را شامل میشود
    """

    # UNIT_CHOICES = [
    #     ("تعداد" , "تعداد"),
    #     ("هکتار" , "هکتار"),
    #     ("نفرماه" , "نفرماه"),
    #     ("متراژ" , "متراژ"),
    #     ("کیلومترمربع" , "کیلومترمربع"),
    # ]
    FAZ_CHOICES = [
        (1, 'شناسایی'),
        (2, 'پیجویی'),
        (3, 'نیمه تفصیلی'),
        (4, 'تفصیلی'),
    ]
    faz = models.PositiveIntegerField(
        verbose_name="فاز",
        choices=FAZ_CHOICES,
        null=True,
        blank=True,
    )

    title = models.CharField(
        verbose_name="عنوان بند شرح خدمات",
        max_length=250,
        blank=False,
        null=False,
        unique=False,
    )
    # unit = models.CharField( # نداریم
    #     verbose_name="واحد",
    #     max_length=100,
    #     choices=UNIT_CHOICES,
    #     blank=False,
    #     null=False,
    # )
    percentage = models.FloatField(
        verbose_name="درصد بند",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False,
        blank=False
    )
    # total_volume = models.PositiveIntegerField( # نداریم
    #     verbose_name="حجم کل بند",
    #     default=0,
    #     null=False,
    #     validators=[MinValueValidator(0)],
    #     blank=False,
    # )
    worked_percentage = models.FloatField(
        verbose_name="درصد کار",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False,
        blank=False,
    )
    # unit_price = models.PositiveBigIntegerField( # نداریم
    #     verbose_name="قیمت واحد",
    #     default=0,
    #     null=False,
    #     blank=False,
    # )
    contract = models.ForeignKey(
        Contract,
        verbose_name="قرارداد",
        on_delete=models.CASCADE,
        related_name='shrh_items',
        null=False,
        blank=False,
    )

    @property
    def completion_percentage(self):
        """Calculate completion percentage"""
        if self.percentage == 0:
            return 0
        return max(min((self.worked_percentage / self.percentage) * 100, 100), 0)
    
    @property
    def remaining_percentage(self):
        """Calculate remaining work percentage"""
        return max(self.percentage - self.worked_percentage, 0)
    
    @property
    def total_price(self):
        mablagh = self.contract.mablagh or 0
        return round((mablagh * self.percentage) / 100, 2)

    @property
    def completed_price(self):
        mablagh = self.contract.mablagh or 0
        return round((mablagh * self.worked_percentage) / 100, 2)

    def clean(self):
        """Custom validation"""
        pass


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.contract.title} بند {self.title}"
    
    class Meta:
        verbose_name = "بند  شرخ‌خدمات"
        verbose_name_plural = "بندهای شرح‌خدمات"
        indexes = [
            models.Index(fields=['contract']),
        ]

class ShrhLayer(CustomModel):
    """
        لایه های مربوط به هر بند از شرح خدمات
        هر بند از شرح خدمات میتواند به  چند لایه وصل باشد
        هر لایه شرح خدماتی مختص به یک شرح حدمات است
    """
    UNIT_CHOICES = [
        ("تعداد" , "تعداد"),
        ("هکتار" , "هکتار"),
        ("نفرماه" , "نفرماه"),
        ("متراژ" , "متراژ"),
        ("کیلومترمربع" , "کیلومترمربع"),
    ]
    
    shrh_base = models.ForeignKey(
        ShrhBase,
        on_delete=models.CASCADE,
        related_name="shr_layers",
        null=False,
        blank=False,
    )
    oldid = models.IntegerField( # the is for migrate from old to new db
        primary_key=False,
        unique=False,
        blank=True,
        null=True
    )
    layer_name = models.ForeignKey(
        LayersNames,
        on_delete=models.CASCADE,
        related_name="layer_shrlyrs",
        null=False,
        blank=False,
    )
    raster_uuid = models.CharField(
        verbose_name="raster uuid" ,
        max_length=100,
        blank=True,
        null=True,
    )
    scale = models.IntegerField(
        verbose_name="مقیاس",
        choices=SCALE_CHOICES,
        blank=True,
        null=True,
    )

    unit = models.CharField(
        verbose_name="واحد",
        max_length=100,
        choices=UNIT_CHOICES,
        blank=True,
        null=True,
    )

    unit_price = models.PositiveBigIntegerField(
        verbose_name="قیمت واحد",
        default=0,
        null=False,
        blank=False,
    )

    layer_weight = models.PositiveIntegerField(
        verbose_name="وزن لایه",
        default=0,
        validators=[MinValueValidator(0)],
        null=False,
        blank=False
    )
    layer_volume = models.PositiveIntegerField(
        verbose_name="حجم لایه",
        default=0,
        null=False,
        validators=[MinValueValidator(0)],
        blank=False,
    )
    is_uploaded = models.BooleanField(
        verbose_name="بارگذاری شده",
        default=False,
        null=False,
        blank=False,
    )
    last_uploaded_date = models.DateTimeField(
        verbose_name="تاریخ آخرین بارگذاری",
        null=True,
        blank=True
    )
    last_uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="کاربر بارگذاری کننده",
        related_name="uploader_shrh_layers",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    upload_count = models.PositiveIntegerField(
        verbose_name="تعداد دفعات بارگذاری",
        default=0,
        null=False,
        blank=False
    )
    is_verified = models.BooleanField(
        verbose_name="تایید نهایی",
        default=False,
        blank=False,
        null=False
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="کاربر تاییدنهایی کننده",
        related_name="verified_shrh_layers",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    verified_at = models.DateTimeField(
        verbose_name="تاریخ تاییدنهایی شده",
        null=True,
        blank=True,
    )
    contractborder = models.ForeignKey(
        'contracts.ContractBorder',
        on_delete=models.CASCADE,
        related_name="rcontractborderlayers",
        blank=False,
        null=False,
        db_index=True,
    )

    @property
    def status(self):
        """Get current status of the layer"""
        if self.is_verified:
            return "تایید شده"
        elif self.is_uploaded:
            return "بارگذاری شده"
        else:
            return "در انتظار بارگذاری"
        
    @property
    def can_be_verified(self):
        """Check if layer can be verified"""
        return self.is_uploaded and not self.is_verified

    def __str__(self):
        base = getattr(self, "shrh_base", None)
        layer = getattr(self, "layer_name", None)
        if base and layer:
            return f"{base.title} لایه {layer.layername_en}"
        return "لایه شرح خدمات"
    
    def clean(self):
        """Custom validation"""
        if self.is_verified and not self.is_uploaded:
            raise ValidationError({
                'is_verified': 'لایه باید ابتدا بارگذاری شود تا بتوان آن را تایید کرد'
            })
        
        # If verified, must have verifier and date
        if self.is_verified:
            if not self.verified_by:
                raise ValidationError({
                    'verified_by': 'برای تایید لایه باید کاربر تایید کننده مشخص شود'
                })
            if not self.verified_at:
                raise ValidationError({
                    'verified_at': 'برای تایید لایه باید تاریخ تایید مشخص شود'
                })
        
        # If not verified, clear verification data
        if not self.is_verified:
            if self.verified_by or self.verified_at:
                self.verified_by = None
                self.verified_at = None

        if self.contractborder and self.shrh_base and \
            self.contractborder.contract != self.shrh_base.contract:

            raise ValidationError({
                "contractborder": "قراردادی که این محدوده قرارداد به آن متصل است با قراردادی که شرح خدمات این لایه به آن متصل است متفاوت است"
            })
    
    def mark_as_uploaded(self , user):
        """Mark layer as uploaded and update timestamp"""
        from django.utils import timezone
        
        self.is_uploaded = True
        self.last_uploaded_date = timezone.now()
        self.last_uploaded_by = user 
        self.upload_count += 1
        self.save(update_fields=['is_uploaded', 'last_uploaded_by' , 'last_uploaded_date', 'upload_count'])
    
    def verify(self, user):
        """Verify the layer by a user"""
        from django.utils import timezone
        
        if not self.is_uploaded:
            raise ValidationError("لایه باید ابتدا بارگذاری شود")
        
        self.is_verified = True
        self.verified_by = user
        self.verified_at = timezone.now()
        self.save(update_fields=['is_verified', 'verified_by', 'verified_at'])
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "لایه شرح خدمات"
        verbose_name_plural = "لایه‌های شرح خدمات"
        ordering = ['shrh_base', 'layer_name']


