"""
contracts/models/SharhKhadamats.py
==================================

این فایل همهٔ مدل‌های «شرح خدمات» قرارداد را در بر دارد.

نقشهٔ کلی مدل‌ها (از کاتالوگ ثابت تا کار انجام‌شده):

    Faz ─┐
    Vahed ─┼─► ShrhCatalog  (کاتالوگ ثابت، از اکسل)
           │        ▲
           │        │ انتخاب توسط سازمان همراه با وزن (و مقیاس)
           │        │
    Contract ──► ShrhContract ──► ShrhLayer (لایه‌ها)
       │              │
       │              │ اختصاص توسط مشاور ارشد
       │              ▼
       ├──► SherkatContract ◄── EkhtesasShrh (بستهٔ کار + کادر MultiPolygon)
       │          │
       │          └─► NaghshSherkat (ناظر، پیمانکار، ...)
       │
       └──► moshaver_arshad (Sherkat)   ← فیلد روی خود Contract



نکته: چون Contract.shrh_items دیگر به ShrhCatalog وصل نیست، هر جای دیگری که
   `contract.shrh_items` را به‌عنوان «بند کاتالوگ» می‌خواند باید به
   ShrhContract (که شرح‌خدمات واقعی قرارداد است) تغییر کند؛ related_name همان مانده.
"""

from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum

from common.constants import SCALE_CHOICES
from common.models.models import CustomModel
from contracts.models.models import ContractDomin,Contract
# from layers.models.models import LayersNames


# ════════════════════════════════════════════════════════════════════
# ۱) جداول پایه: فاز و واحد
# ════════════════════════════════════════════════════════════════════

class Faz(CustomModel):
    """
    فازهای اکتشاف: شناسایی، پی‌جویی، عمومی، تفصیلی.

    به‌جای choices ثابت در کد، جدول جداست تا بعداً بدون migration بتوان
    فاز جدید اضافه کرد. فیلد `order` ترتیب نمایش فازها را مشخص می‌کند.
    مقدارها از ردیف‌های سطح فاز اکسل (نارنجی) ساخته می‌شوند.
    """
    title = models.CharField(
        verbose_name="عنوان فاز",
        max_length=100,
        unique=True,
        error_messages={'unique': "فازی با این عنوان هم‌اکنون وجود دارد"},
    )
    order = models.PositiveIntegerField(verbose_name="ترتیب", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "فاز"
        verbose_name_plural = "فازها"
        ordering = ['order']


class Vahed(CustomModel):
    """
    واحد اندازه‌گیری بندها: نسخه، نمونه، متر، مترمکعب، ایستگاه، کیلومتر خطی،
    هکتار، دستگاه/ساعت، ...

    مقدارها از ستون «واحد» اکسل می‌آیند. جدول جداست تا بدون migration
    قابل افزودن باشد.
    """
    title = models.CharField(
        verbose_name="عنوان واحد",
        max_length=100,
        unique=True,
        error_messages={'unique': "واحدی با این عنوان هم‌اکنون وجود دارد"},
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "واحد"
        verbose_name_plural = "واحدها"


# ════════════════════════════════════════════════════════════════════
# ۲) کاتالوگ ثابت شرح خدمات (همان اکسل)
# ════════════════════════════════════════════════════════════════════

class ShrhCatalog(CustomModel):
    """
    کاتالوگ ثابت شرح خدمات؛ هر رکورد یک سطر از اکسل است.

    - این جدول مستقل از قرارداد است و فقط یک‌بار (seed) از اکسل پر می‌شود.
    - ساختار درختی دارد: «گروه» (مثلاً مطالعات ژئوشیمی) چند «بند» (مثلاً آنالیز
      شیمیایی نمونه‌ها) دارد. گروه‌ها `is_onvan_asli=True` و واحد ندارند.
    - عنوان‌ها تکراری‌اند (مثلاً «آنالیز شیمیایی نمونه‌ها» در چند فاز)، بنابراین
      عنوان unique نیست و شناسهٔ یکتا همان ستون «ردیف» اکسل (`code`) است.
    - فاز بالاترین سطح است و در جدول Faz نگهداری می‌شود، نه در درخت.
      بعضی بندها مستقیماً زیر فاز هستند، پس `parent` اختیاری است.
    - وزن (درصد) و مقدار اینجا نیست؛ آن‌ها مخصوص هر قرارداد است (ShrhContract).
    """
    contract_domin = models.ForeignKey(
        ContractDomin,
        verbose_name="نوع قرارداد",
        on_delete=models.PROTECT,
        related_name="rshrhcatalogha",
        blank=False,
        null=False,
    )

    faz = models.ForeignKey(
        Faz,
        verbose_name="فاز",
        on_delete=models.PROTECT,
        related_name="rbandha",
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="عنوان اصلی",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
        limit_choices_to={"is_onvan_asli": True},
    )
    is_onvan_asli = models.BooleanField(
        verbose_name="عنوان اصلی است",
        default=False,
        help_text="گروه‌ها فقط عنوان‌دهنده‌اند و به قرارداد اختصاص داده نمی‌شوند.",
    )
    title = models.CharField(
        verbose_name="عنوان",
        max_length=250,
    )
    vahed = models.ForeignKey(
        Vahed,
        verbose_name="واحد اندازه‌گیری",
        on_delete=models.PROTECT,
        related_name="rbandha",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="توضیحات",
        blank=True,
        default="",
    )
    order = models.PositiveIntegerField(
        verbose_name="ترتیب نمایش",
        default=0,
    )

    def clean(self):
        errors = {}
        if self.parent_id:
            if not self.parent.is_onvan_asli:
                errors['parent'] = "عنوان اصلی باید یک عنوان اصلی باشد."
            elif self.parent.faz_id != self.faz_id:
                errors['faz'] = "فاز بند باید با فاز عنوان اصلی یکی باشد."
        if self.is_onvan_asli and self.vahed_id:
            errors['vahed'] = "عنوان اصلی واحد اندازه گیری ندارد."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        prefix = "📁" if self.is_onvan_asli else "↳"
        return f"{prefix} {self.faz} | {self.title}"

    class Meta:
        verbose_name = "بند کاتالوگ شرح خدمات"
        verbose_name_plural = "کاتالوگ شرح خدمات"
        ordering = ['order']


# ════════════════════════════════════════════════════════════════════
# ۳) نقش و شرکت‌های درگیر در قرارداد
# ════════════════════════════════════════════════════════════════════

class NaghshSherkat(CustomModel):
    """
    نقش یک شرکت در قرارداد: ناظر، پیمانکار، پیمانکار اکتشاف، پیمانکار حفاری، ...
    (ممکن است یک شرکت در یک قرارداد ناظر باشد در قراردادی دیگر مشاور)

    - «مشاور ارشد» اینجا نیست؛ آن فیلد `Contract.moshaver_arshad` است.
    - جدول جداست تا نقش جدید بدون migration اضافه شود.
    """
    title = models.CharField(
        verbose_name="عنوان نقش",
        max_length=100,
        unique=True,
        error_messages={'unique': "نقشی با این عنوان هم‌اکنون وجود دارد"},
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "نقش شرکت"
        verbose_name_plural = "نقش‌های شرکت"


class SherkatContract(CustomModel):
    """
    حضور یک شرکت با یک نقش مشخص در یک قرارداد.

    - فقط کاربران «مشاور ارشد همان قرارداد» (کاربرهای شرکت Contract.moshaver_arshad)
      اجازهٔ ساخت و ویرایش این رکوردها را دارند (در لایهٔ API/permission بررسی می‌شود).
    - یک شرکت می‌تواند در یک قرارداد چند نقش داشته باشد (مثلاً هم پیمانکار اکتشاف
      هم پیمانکار حفاری) ولی تکرار دقیقاً یک شرکت+نقش ممنوع است.
    - خود مشاور ارشد قرارداد نمی‌تواند اینجا ثبت شود (او بند اجرایی نمی‌گیرد).
    """
    contract = models.ForeignKey(
        Contract,
        verbose_name="قرارداد",
        on_delete=models.CASCADE,
        related_name="rsherkatha",
    )
    sherkat = models.ForeignKey(
        "common.Sherkat",
        verbose_name="شرکت",
        on_delete=models.PROTECT,
        related_name="rnaghshha",
    )
    naghsh = models.ForeignKey(
        NaghshSherkat,
        verbose_name="نقش",
        on_delete=models.PROTECT,
        related_name="rsherkatha",
    )

    def clean(self):
        if self.contract_id and self.sherkat_id:
            if self.contract.moshaver_arshad_id == self.sherkat_id:
                raise ValidationError({
                    'sherkat': "مشاور ارشد قرارداد نمی‌تواند به‌عنوان شرکت اجرایی ثبت شود."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sherkat} ({self.naghsh}) - {self.contract.title}"

    class Meta:
        verbose_name = "شرکت قرارداد"
        verbose_name_plural = "شرکت‌های قرارداد"
        constraints = [
            models.UniqueConstraint(
                fields=['contract', 'sherkat', 'naghsh'],
                name='uniq_sherkat_naghsh_per_contract',
            ),
        ]


# ════════════════════════════════════════════════════════════════════
# ۴) بستهٔ کار: اختصاص بندها به یک شرکت همراه با کادر
# ════════════════════════════════════════════════════════════════════

class EkhtesasShrh(CustomModel):
    """
    یک «بستهٔ کار» که مشاور ارشد به یک شرکت قرارداد می‌دهد:
    «در این قرارداد، این شرکت با این نقش، این چند بند را در این کادر انجام دهد.»

    - کادر یک MultiPolygon است و هنگام ساخت بسته بارگذاری می‌شود. ربطی به
      InitialBorder یا اکسل ندارد.
    - مقیاس کادر در `scale` ثبت می‌شود. همهٔ بندهای بسته (ShrhContract.ekhtesas)
      باید همین مقیاس را داشته باشند.
    - بندها از سمت ShrhContract به این بسته وصل می‌شوند
      (related_name = rbandha). هر بند فقط یک بسته دارد.
    - یک شرکت می‌تواند در یک قرارداد چند بسته (چند کادر) داشته باشد.
    """
    sherkat_contract = models.ForeignKey(
        SherkatContract,
        verbose_name="شرکت قرارداد",
        on_delete=models.CASCADE,
        related_name="rekhtesasha",
    )
    kader = gis_models.MultiPolygonField(
        verbose_name="کادر",
        srid=3857,
    )
    kader_name = models.CharField(
        verbose_name="نام کادر",
        max_length=250,
        blank=True,
        default="",
    )
    scale = models.IntegerField(
        verbose_name="مقیاس کادر",
        choices=SCALE_CHOICES,
        blank=True,
        null=True,
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="اختصاص‌دهنده",
        on_delete=models.SET_NULL,
        related_name="rekhtesasha",
        blank=True,
        null=True,
    )

    @property
    def contract(self):
        return self.sherkat_contract.contract

    @property
    def vazn_kol(self):
        """مجموع وزن بندهای این بسته در قرارداد."""
        return self.rbandha.aggregate(s=Sum('percentage'))['s'] or 0

    @property
    def pishraft(self):
        """پیشرفت وزنی بسته (۰ تا ۱۰۰) = مجموع درصد کار / مجموع وزن."""
        agg = self.rbandha.aggregate(w=Sum('worked_percentage'), p=Sum('percentage'))
        if not agg['p']:
            return 0
        return max(min((agg['w'] or 0) / agg['p'] * 100, 100), 0)

    def __str__(self):
        return f"{self.sherkat_contract} - {self.kader_name or 'کادر'}"

    class Meta:
        verbose_name = "اختصاص شرح خدمات"
        verbose_name_plural = "اختصاص‌های شرح خدمات"


# ════════════════════════════════════════════════════════════════════
# ۵) شرح خدمات واقعی هر قرارداد
# ════════════════════════════════════════════════════════════════════

class ShrhContract(CustomModel):
    """
    یک بند از کاتالوگ که برای یک قرارداد انتخاب شده است (جایگزین SharhBase قدیمی).

    - سازمان هنگام ساخت قرارداد بندها را از ShrhCatalog انتخاب و «وزن» هر کدام
      (percentage) را مشخص می‌کند.
    - یک بند کاتالوگ در یک قرارداد می‌تواند چند بار بیاید، به‌شرط آن‌که مقیاسش
      فرق کند (مثلاً بند A با مقیاس ۱۰۰۰ و بند A با مقیاس ۵۰۰). برای بندهای
      بدون مقیاس فقط یک رکورد مجاز است. (دو UniqueConstraint پایین)
    - `ekhtesas` (اختیاری) نشان می‌دهد بند در کدام بستهٔ کار و به کدام شرکت
      داده شده است؛ خالی یعنی هنوز به کسی اختصاص داده نشده.
    - `worked_percentage` درصد کار انجام‌شده‌ از وزن این بند است.
    """
    contract = models.ForeignKey(
        Contract,
        verbose_name="قرارداد",
        on_delete=models.CASCADE,
        related_name='shrh_items',
    )
    shrh_catalog = models.ForeignKey(
        ShrhCatalog,
        verbose_name="بند کاتالوگ",
        on_delete=models.PROTECT,
        related_name="rqarardadha",
        limit_choices_to={'is_onvan_asli': False},
    )
    scale = models.IntegerField(
        verbose_name="مقیاس",
        choices=SCALE_CHOICES,
        blank=True,
        null=True,
    )
    percentage = models.FloatField(
        verbose_name="وزن بند (درصد)",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    worked_percentage = models.FloatField(
        verbose_name="درصد کار",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    ekhtesas = models.ForeignKey(
        EkhtesasShrh,
        verbose_name="بستهٔ اختصاص",
        on_delete=models.SET_NULL,
        related_name="rbandha",
        blank=True,
        null=True,
    )

    # ---------- محاسبات ----------
    @property
    def vahed(self):
        return self.shrh_catalog.vahed

    @property
    def completion_percentage(self):
        """درصد تکمیل این بند نسبت به وزنش (۰ تا ۱۰۰)."""
        if self.percentage == 0:
            return 0
        return max(min((self.worked_percentage / self.percentage) * 100, 100), 0)

    @property
    def remaining_percentage(self):
        """وزن باقی‌ماندهٔ کار."""
        return max(self.percentage - self.worked_percentage, 0)

    @property
    def total_price(self):
        mablagh = self.contract.mablagh or 0
        return round((mablagh * self.percentage) / 100, 2)

    @property
    def completed_price(self):
        mablagh = self.contract.mablagh or 0
        return round((mablagh * self.worked_percentage) / 100, 2)

    # ---------- اعتبارسنجی ----------
    def clean(self):
        errors = {}
        if self.shrh_catalog_id and self.shrh_catalog.is_onvan_asli:
            errors['shrh_catalog'] = "گروه قابل انتخاب نیست؛ باید یک بند انتخاب شود."
        if self.ekhtesas_id:
            if self.ekhtesas.sherkat_contract.contract_id != self.contract_id:
                errors['ekhtesas'] = "این بسته متعلق به قرارداد دیگری است."
            elif (self.ekhtesas.scale is not None and self.scale is not None
                  and self.ekhtesas.scale != self.scale):
                errors['scale'] = "مقیاس بند با مقیاس کادر بسته یکی نیست."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.contract.title} - {self.shrh_catalog.title}"

    class Meta:
        verbose_name = "بند شرح خدمات قرارداد"
        verbose_name_plural = "بندهای شرح خدمات قرارداد"
        indexes = [models.Index(fields=['contract'])]
        constraints = [
            # بند دارای مقیاس: هر (قرارداد، بند، مقیاس) فقط یک‌بار
            models.UniqueConstraint(
                fields=['contract', 'shrh_catalog', 'scale'],
                condition=models.Q(scale__isnull=False),
                name='uniq_shrh_with_scale_per_contract',
            ),
            # بند بدون مقیاس: هر (قرارداد، بند) فقط یک‌بار
            models.UniqueConstraint(
                fields=['contract', 'shrh_catalog'],
                condition=models.Q(scale__isnull=True),
                name='uniq_shrh_without_scale_per_contract',
            ),
        ]


# ════════════════════════════════════════════════════════════════════
# ۶) لایه‌های هر بند
# ════════════════════════════════════════════════════════════════════

class ShrhLayer(CustomModel):
    """
    لایه‌های مربوط به یک بند از شرح خدمات قرارداد.

    - هر بند قرارداد (ShrhContract) می‌تواند چند لایه داشته باشد و هر لایه
      مخصوص همان بند است. لایه‌ها دستی و بعداً انتخاب می‌شوند.
    - واحد و مقیاس لایه دیگر فیلد جدا ندارد؛ از بند می‌آید
      (واحد از کاتالوگ، مقیاس از ShrhContract).
    - چرخهٔ وضعیت: در انتظار بارگذاری ← بارگذاری شده ← تایید شده.
    """
    shrh_contract = models.ForeignKey(
        ShrhContract,
        verbose_name="بند قرارداد",
        on_delete=models.CASCADE,
        related_name="shr_layers",
    )
    # layer_name = models.ForeignKey(
    #     LayersNames,
    #     on_delete=models.CASCADE,
    #     related_name="layer_shrlyrs",
    # )
    raster_uuid = models.CharField(
        verbose_name="raster uuid",
        max_length=100,
        blank=True,
        null=True,
    )
    unit_price = models.PositiveBigIntegerField(
        verbose_name="قیمت واحد",
        default=0,
    )
    layer_weight = models.PositiveIntegerField(
        verbose_name="وزن لایه",
        default=0,
        validators=[MinValueValidator(0)],
    )
    layer_volume = models.PositiveIntegerField(
        verbose_name="حجم لایه",
        default=0,
        validators=[MinValueValidator(0)],
    )
    is_uploaded = models.BooleanField(verbose_name="بارگذاری شده", default=False)
    last_uploaded_date = models.DateTimeField(
        verbose_name="تاریخ آخرین بارگذاری", null=True, blank=True
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
        verbose_name="تعداد دفعات بارگذاری", default=0
    )
    is_verified = models.BooleanField(verbose_name="تایید نهایی", default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="کاربر تاییدنهایی کننده",
        related_name="verified_shrh_layers",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    verified_at = models.DateTimeField(
        verbose_name="تاریخ تاییدنهایی شده", null=True, blank=True
    )

    @property
    def scale(self):
        return self.shrh_contract.scale

    @property
    def vahed(self):
        return self.shrh_contract.vahed

    @property
    def status(self):
        if self.is_verified:
            return "تایید شده"
        elif self.is_uploaded:
            return "بارگذاری شده"
        return "در انتظار بارگذاری"

    @property
    def can_be_verified(self):
        return self.is_uploaded and not self.is_verified

    def clean(self):
        if self.is_verified and not self.is_uploaded:
            raise ValidationError({
                'is_verified': 'لایه باید ابتدا بارگذاری شود تا بتوان آن را تایید کرد'
            })
        if self.is_verified:
            if not self.verified_by:
                raise ValidationError({
                    'verified_by': 'برای تایید لایه باید کاربر تایید کننده مشخص شود'
                })
            if not self.verified_at:
                raise ValidationError({
                    'verified_at': 'برای تایید لایه باید تاریخ تایید مشخص شود'
                })
        else:
            if self.verified_by or self.verified_at:
                self.verified_by = None
                self.verified_at = None

    def mark_as_uploaded(self, user):
        """علامت‌گذاری لایه به‌عنوان بارگذاری‌شده و ثبت کاربر و زمان."""
        from django.utils import timezone
        self.is_uploaded = True
        self.last_uploaded_date = timezone.now()
        self.last_uploaded_by = user
        self.upload_count += 1
        self.save(update_fields=['is_uploaded', 'last_uploaded_by',
                                 'last_uploaded_date', 'upload_count'])

    def verify(self, user):
        """تایید نهایی لایه توسط یک کاربر (فقط پس از بارگذاری)."""
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

    def __str__(self):
        return f"{self.shrh_contract.shrh_catalog.title} لایه {self.layer_name.layername_en}"

    class Meta:
        verbose_name = "لایه شرح خدمات"
        verbose_name_plural = "لایه‌های شرح خدمات"
        ordering = ['shrh_contract',] #'layer_name'


# ════════════════════════════════════════════════════════════════════
# WORKFLOW — جریان کار کامل از ساخت قرارداد تا تایید لایه‌ها
# ════════════════════════════════════════════════════════════════════
"""
بازیگران
--------
• سازمان (admin / کارفرما): قرارداد را می‌سازد، مشاور ارشد و بندها و وزن‌ها را تعیین می‌کند.
• مشاور ارشد: کاربران شرکتی که در Contract.moshaver_arshad ثبت شده است.
  (تشخیص: request.user.sherkat_id == contract.moshaver_arshad_id)
• شرکت اجرایی: ناظر، پیمانکار، پیمانکار اکتشاف، پیمانکار حفاری و ... .
  کاربران آن‌ها همان کاربرانی‌اند که User.sherkat برابر شرکتشان است.

مرحله ۰ — آماده‌سازی داده‌های ثابت (یک‌بار، توسط توسعه‌دهنده)
    • جدول Faz از ردیف‌های سطح فاز اکسل ساخته می‌شود:
      شناسایی، پی‌جویی، عمومی، تفصیلی (با order).
    • جدول Vahed از ستون «واحد» اکسل پر می‌شود (مقادیر یکتا، بعد از strip).
    • ShrhCatalog از روی ردیف‌های اکسل پر می‌شود (management command یا data migration):
        - ستون «ردیف» ← code
        - سطرهای Bold بدون واحد ← is_onvan_asli=True ؛ سطرهای غیر Bold ← بند (is_onvan_asli=False)
        - parent: نزدیک‌ترین گروه بالاتر در همان فاز؛ اگر نبود parent=None
        - faz: فازی که سطر زیر آن قرار دارد
        - vahed و description از ستون‌های «واحد» و «توضیحات»
      ناهمخوانی‌های اکسل قبل از seed باید با رئیس مرور شود:
        ردیف ۳۴ (بدون واحد)، و جایگاه ردیف‌های ۱۳۴ تا ۱۴۶ (گروه یا زیر فاز؟).
    • NaghshSherkat و NoeKhadamat با مقادیر اولیه ساخته می‌شوند
      (ناظر، پیمانکار، پیمانکار اکتشاف، پیمانکار حفاری، ...).
    • برای شرکت‌هایی که می‌توانند مشاور ارشد شوند Sherkat.mojaz_moshaver_arshad=True می‌شود.

مرحله ۱ — ساخت قرارداد (سازمان)
    • سازمان Contract را با عنوان، شماره، تاریخ‌ها، مبلغ و ... می‌سازد.
    • Contract.moshaver_arshad را از میان شرکت‌های دارای mojaz_moshaver_arshad=True
      انتخاب می‌کند. از این لحظه کاربران آن شرکت «مشاور ارشد این قرارداد» محسوب می‌شوند.

مرحله ۲ — انتخاب شرح خدمات و تعیین وزن (سازمان)
    • سازمان از کاتالوگ ShrhCatalog (فقط is_onvan_asli=False) بندهای این قرارداد را انتخاب می‌کند.
      برای هر انتخاب یک ShrhContract ساخته می‌شود با:
        - percentage = وزن بند (توسط سازمان)
        - scale = مقیاس (در صورت نیاز)
    • اگر بندی باید در دو مقیاس انجام شود، دو رکورد جدا ساخته می‌شود
      (مثلاً A با مقیاس ۱۰۰۰ و A با مقیاس ۵۰۰) و هرکدام وزن خودش را دارد.
    • در لایهٔ سرویس/serializer بررسی شود که مجموع percentage بندهای هر قرارداد از ۱۰۰ بیشتر نشود
      (اینکه حتماً برابر ۱۰۰ باشد یا نه، هنوز تصمیم نگرفته‌ایم).
    • در این مرحله ekhtesas هنوز خالی است (بند به هیچ‌کس داده نشده).

مرحله ۳ — تعیین شرکت‌های قرارداد (کاربر مشاور ارشد)
    • مشاور ارشد برای هر شرکت یک SherkatContract می‌سازد: (قرارداد + شرکت + نقش).
    • اعتبارسنجی: خود مشاور ارشد نمی‌تواند اینجا ثبت شود؛ تکرار شرکت+نقش ممنوع؛
      یک شرکت می‌تواند با چند نقش مختلف ثبت شود.

مرحله ۴ — اختصاص بندها و بارگذاری کادر (کاربر مشاور ارشد)
    برای هر شرکت و هر کادر:
      ۱. یک EkhtesasShrh ساخته می‌شود: sherkat_contract، kader (MultiPolygon بارگذاری‌شده)،
         kader_name، scale، assigned_by.
      ۲. بندهایی از ShrhContract همین قرارداد که هنوز ekhtesas ندارند انتخاب می‌شوند
         و ekhtesas آن‌ها روی همین بسته ست می‌شود.
    قواعد (در ShrhContract.clean بررسی می‌شود):
      • بند باید متعلق به همان قرارداد بسته باشد.
      • مقیاس بند و مقیاس کادر در صورت وجود باید برابر باشد.
      • هر بند فقط در یک بسته (یک شرکت و یک کادر) قرار می‌گیرد؛
        برای کادر دوم با مقیاس دیگر، رکورد ShrhContract دیگری (با آن مقیاس) استفاده می‌شود.
      • یک شرکت می‌تواند در یک قرارداد چند بسته (چند کادر) داشته باشد.
    مثال: قرارداد X، شرکت P با نقش «پیمانکار حفاری»:
        بستهٔ ۱: کادر B، مقیاس ۱۰۰۰ ← سه بند از حفریات زیرسطحی
        بستهٔ ۲: کادر C، مقیاس ۵۰۰   ← همان بند تکراری با مقیاس ۵۰۰

مرحله ۵ — اجرا و بارگذاری لایه‌ها (کاربران شرکت اجرایی)
    • کاربران هر شرکت فقط بسته‌ها و بندهای شرکت خودشان
      (SherkatContract.sherkat == request.user.sherkat) را می‌بینند.
    • لایه‌ها (ShrhLayer) برای هر ShrhContract به‌صورت دستی انتخاب/ساخته می‌شوند
      (طراحی انتخاب لایه‌ها بعداً مشخص می‌شود).
    • بارگذاری با ShrhLayer.mark_as_uploaded(user) انجام می‌شود:
      is_uploaded=True، ثبت کاربر و زمان، افزایش upload_count.
    • با هر بارگذاری/پیشرفت، worked_percentage بند به‌روز می‌شود
      (روش دقیق محاسبه — از روی لایه‌ها یا دستی — باید مشخص شود).

مرحله ۶ — تایید (ناظر / مشاور ارشد)
    • لایهٔ بارگذاری‌شده با ShrhLayer.verify(user) تایید نهایی می‌شود
      (is_verified، verified_by، verified_at).
    • وضعیت لایه: «در انتظار بارگذاری» ← «بارگذاری شده» ← «تایید شده».
    • اینکه چه کسی حق تایید دارد (ناظر یا مشاور ارشد) در permission تعیین می‌شود
      و در مدل محدودیتی ندارد.

مرحله ۷ — گزارش پیشرفت
    • پیشرفت هر بند:    ShrhContract.completion_percentage و remaining_percentage
    • پیشرفت هر بسته:   EkhtesasShrh.pishraft (میانگین وزنی بندهای بسته)
    • مبالغ:            ShrhContract.total_price و completed_price
                        (برپایهٔ Contract.mablagh × درصد)
    • پیشرفت کل قرارداد: مجموع worked_percentage بندها
                        (قابل نگاشت به Contract.progress)

نکات مهم
    • حذف: حذف قرارداد، بندها و شرکت‌های آن را هم پاک می‌کند (CASCADE).
      حذف یک بسته فقط ekhtesas بندها را خالی می‌کند (SET_NULL)، خود بندها می‌مانند.
    • حذف Faz/Vahed/ShrhCatalog/NaghshSherkat/Sherkat در صورت استفاده شدن مجاز نیست (PROTECT).
    • تغییر مشاور ارشد یک قرارداد: اگر مشاور جدید قبلاً در SherkatContract همان قرارداد
      بوده باشد، باید قبل از تغییر آن رکورد حذف شود (در Contract.clean چک می‌شود).
    • برای استفاده در admin/API، همهٔ save ها full_clean() را اجرا می‌کنند؛
      بنابراین bulk_create و update() آن‌ها را دور می‌زند (فقط در seed کاتالوگ استفاده شود).
"""