from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from common.models import CustomModel
from initialborders.models.models import InitialBorder , InitialBorderDomin

class AmarKarKhaneh(CustomModel):
    ALLOWED_INITBORDER_CODES = [808 , 1002]  # Alloewd Initialborder Domain Code (صنعتی و فرآوری)

    initialborder = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="rinitborderamarkarkhaneh",
        blank=False,
        null=False
    )

    sal = models.IntegerField(verbose_name="سال" , null=False,blank=False)
    doure = models.IntegerField(verbose_name="دوره" , validators=[
            MinValueValidator(1, message="دوره نمی‌تواند کمتر از 1 باشد."),
            MaxValueValidator(12, message="دوره نمی‌تواند بیشتر از 12 باشد.")
        ],null=False,blank=False)
    name_mahsoul = models.CharField(verbose_name="نام محصول" , max_length=255 , null=False,blank=False)

    zarfiyat_amaliyati = models.FloatField(verbose_name="ظرفیت عملیاتی" , default=0)
    mahsoul_kham_daryafti = models.FloatField(verbose_name="محصول خام دریافتی",default=0)
    mizain_toulid = models.FloatField(verbose_name="میزان تولید",default=0)
    hazine_toulid = models.FloatField(verbose_name="هزینه تولید",default=0)
    masraf_ab = models.FloatField(verbose_name="میانگین مصرف آب" , default=0 ,)
    masraf_bargh = models.FloatField(verbose_name="میانگین مصرف برق" , default=0 ,)
    masraf_soukht = models.FloatField(verbose_name="مجموع مصرف سوخت" , default=0 ,)
    masraf_gaz = models.FloatField(verbose_name="میانگین مصرف گاز" , default=0 ,)
    masraf_mavad = models.FloatField(verbose_name="میانگین ممصرف مواد اولیه" , default=0 ,)
    
    def clean(self):
        super().clean()
        if self.initialborder and self.initialborder.dtyp:
            if self.initialborder.dtyp.code not in self.ALLOWED_INITBORDER_CODES:
                raise ValidationError({
                    'initialborder': f'فقط محدوده اولیه با کدهای {self.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                })
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"آمار کارخانه {self.initialborder.title}"
    
    class Meta:
        verbose_name = "آمار کارخانه"
        verbose_name_plural = "امارهای کارخانه"
        constraints = [
                models.UniqueConstraint(
                    fields=['initialborder','sal', 'doure', 'name_mahsoul'], 
                    name='unique_sal_doure_mahsoul',
                    violation_error_message='ترکیب سال، دوره و نام محصول قبلاً ثبت شده است.'
                )
            ]
        
class AmarEstekhraj(CustomModel):
    ALLOWED_INITBORDER_CODES = [55 , 1003]  # Alloewd Initialborder Domain Code (پروانه بهره برداری , استخراجی)


    initialborder = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="rinitborderamarestekhraj",
        blank=False,
        null=False
    )

    sal = models.IntegerField(verbose_name="سال" , null=False,blank=False)
    doure = models.IntegerField(verbose_name="دوره" , validators=[
            MinValueValidator(1, message="دوره نمی‌تواند کمتر از 1 باشد."),
            MaxValueValidator(12, message="دوره نمی‌تواند بیشتر از 12 باشد.")
        ],null=False,blank=False)
    
    made_madani_estekhraji = models.FloatField(verbose_name="ماده معدنی استخراجی طبق طرح" , default=0)
    ayar_made_madani = models.FloatField(verbose_name="عیار ماده معدنی" , default=0)
    estekhraj_vaghei = models.FloatField(verbose_name="میزان استخراج واقعی",default=0)
    motavaset_ayar_estekhraji = models.FloatField(verbose_name="متوسط عیار استخراجی",default=0)
    mizan_batele_bardari = models.FloatField(verbose_name="میزان یاطله برداری",default=0)
    hazine_estekhraj = models.FloatField(verbose_name="هزینه استخراج",default=0)
    darsad_amalkard = models.FloatField(verbose_name="درصد عملکرد به برنامه سال",default=0)

    def clean(self):
        super().clean()
        if self.initialborder and self.initialborder.dtyp:
            if self.initialborder.dtyp.code not in self.ALLOWED_INITBORDER_CODES:
                raise ValidationError({
                    'initialborder': f'فقط محدوده اولیه با کدهای {self.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                })

    def __str__(self):
        return f"آمار استخراج {self.initialborder.title}"
    
    class Meta:
        verbose_name = "آمار استخراج"
        verbose_name_plural = "امارهای استخراج"
        constraints = [
                models.UniqueConstraint(
                    fields=['initialborder','sal', 'doure',], 
                    name='unique_sal_doure_estekhraj',
                    violation_error_message='ترکیب سال، دوره قبلاً ثبت شده است.'
                )
            ]
        
class HSEPASMAND(CustomModel):
    """
        HSE پسماند
    """

    initialborder = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="rinitborderamarhsepasmand",
        blank=False,
        null=False
    )

    sal = models.IntegerField(verbose_name="سال" , null=False,blank=False)
    doure = models.IntegerField(verbose_name="دوره" , validators=[
            MinValueValidator(1, message="دوره نمی‌تواند کمتر از 1 باشد."),
            MaxValueValidator(12, message="دوره نمی‌تواند بیشتر از 12 باشد.")
        ],null=False,blank=False)
    
    onvan_pasmand = models.CharField(verbose_name="عنوان پسماند" , max_length=255,null=True,blank=True)
    noe_passmand = models.CharField(verbose_name="عنوان پسماند" , max_length=255,null=True,blank=True)
    vazn = models.FloatField(verbose_name="وزن", default=0)

    def clean(self):
        super().clean()

    def __str__(self):
        return f"آمار HSE پسماند {self.initialborder.title}"
    
    class Meta:
        verbose_name = "آمار HSE پسماند"
        verbose_name_plural = "امارهای HSE پسماند"
        constraints = [
                models.UniqueConstraint(
                    fields=['initialborder','sal', 'doure',], 
                    name='unique_sal_doure_hsepasmand',
                    violation_error_message='ترکیب سال، دوره قبلاً ثبت شده است.'
                )
            ]
        
class HSEHADESE(CustomModel):
    """
        HSE حادثه
    """

    initialborder = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="rinitborderamarhsehadese",
        blank=False,
        null=False
    )

    sal = models.IntegerField(verbose_name="سال" , null=False,blank=False)
    
    shadid = models.IntegerField(verbose_name="تعداد حوادث شدید" , default=0)
    fout = models.IntegerField(verbose_name="تعدا افراد فوت شده" , default=0)
    elat = models.CharField(verbose_name="علت حادثه", max_length=500 , blank=True , null=True)

    def clean(self):
        super().clean()

    def __str__(self):
        return f"آمار HSE حادثه {self.initialborder.title}"
    
    class Meta:
        verbose_name = "آمار HSE حادثه"
        verbose_name_plural = "امارهای HSE حادثه"


class AmarEkteshaf(CustomModel):

    initialborder = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="rinitborderamarekteshaf",
        blank=False,
        null=False
    )

    sal = models.IntegerField(verbose_name="سال" , null=False,blank=False)
    doure = models.IntegerField(verbose_name="دوره" , validators=[
            MinValueValidator(1, message="دوره نمی‌تواند کمتر از 1 باشد."),
            MaxValueValidator(12, message="دوره نمی‌تواند بیشتر از 12 باشد.")
        ],null=False,blank=False)
    
    masahat_mored_ekteshaf = models.FloatField(verbose_name="مساحت مورد اکتشاف",default=0)
    darsad_pishraft = models.FloatField(verbose_name="درصد پیشرفت عملیات اکتشاف عمومی تا تفصیلی",default=0)
    hazine_kol = models.FloatField(verbose_name="هزینه کل نسبت به درصد پیشرفت کار",default=0)
    ayar_made_madani = models.FloatField(verbose_name="میانگین عیار ماده مدنی",default=0)

    def clean(self):
        super().clean()

    def __str__(self):
        return f"آمار اکتشاف {self.initialborder.title}"
    
    class Meta:
        verbose_name = "آمار اکتشاف"
        verbose_name_plural = "امارهای اکتشاف"
        constraints = [
                models.UniqueConstraint(
                    fields=['initialborder','sal', 'doure',], 
                    name='unique_sal_doure_amarekteshaf',
                    violation_error_message='ترکیب سال، دوره قبلاً ثبت شده است.'
                )
            ]
        
class AmarAmalkardTajhizCoal(models.Model):
    ALLOWED_INITBORDER_CODES = [737 , ] # زغال


    RAVESH__CHOICES = [(1,'امانی') , (2,'پیمانی یا سرمایه گذار')]
    PEYMANKAR_TYPE_CHOICES = [(1,'حقیقی'),(2,'حقوقی دولتی'),(3,'حقوقی غیر دولتی')]

    initialborder = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="rinitborderamaramalkardtajhizcoal",
        blank=False,
        null=False
    )

    sal = models.IntegerField(verbose_name="سال",null=False,blank=False)
    doure = models.IntegerField(verbose_name="دوره",validators=[
            MinValueValidator(1, message="دوره نمی‌تواند کمتر از 12 باشد."),
            MaxValueValidator(12, message="دوره نمی‌تواند بیشتر از 12 باشد.")
        ],null=False,blank=False)

    zamanstarttajhiz                            = models.IntegerField(verbose_name="زمان شروع تجهیز به سال" , null=True,blank=True)
    reveshejraamaliyatmadani                    = models.IntegerField(verbose_name="روش اجرا عملیات معدنی",choices=RAVESH__CHOICES,blank=True,null=True)
    raveshehdastasisat                          = models.IntegerField(verbose_name="روش اجرا عملیات احداث تاسیسات سطحی",choices=RAVESH__CHOICES,blank=True,null=True)
    namepeymankar                               = models.CharField(verbose_name="نام پیمانکار/سرمایه گذار",blank=True,null=True)
    peymankar_typ                               = models.IntegerField(verbose_name="نوع پیمانکار یا سرمایه گذار",choices=PEYMANKAR_TYPE_CHOICES,blank=False,null=False)
    pishraft_pi_amal_madani_tadoureghabl        = models.FloatField(verbose_name="پیشزفت فیزیکی عملیات معدنی تا پایان دوره قبل درصد",blank=True,null=True)
    pishraft_pi_amal_ehdassathi_tadoureghabl    = models.FloatField(verbose_name="پیشزفت فیزیکی احداث تاسیسات سطحی تا پایان دوره قبل درصد",blank=True,null=True)
    pishraft_pi_amal_taminabobargh_tadoureghabl = models.FloatField(verbose_name="پیشزفت فیزیکی تامیین اب و برق تا پایان دوره قبل درصد",blank=True,null=True)
    pishraft_pi_kol_tadoureghabl                = models.FloatField(verbose_name="پیشزفت فیزیکی کل طرح تجهیز تا پایان دوره قبل درصد",blank=True,null=True)
    amouzehkarkonano_tadoureghabl               = models.FloatField(verbose_name="اموزش کارکنان تا پایان دوره قبل به نفردوره",null=True,blank=True)
    meghdar_zoghal_estekhraj                    = models.FloatField(verbose_name="مقدار زغالسنگ استخراج شده حاصل از عملیات تجهیز تا پایان دوره قبل به تن",null=True,blank=True)
    meghdar_zoghal_zakhire                      = models.FloatField(verbose_name="مقدار ذخیره اماده شده برای استخراج تا پایان دوره قبل به هزارتن",null=True,blank=True)
    
    def clean(self):
        super().clean()
        if self.initialborder and self.initialborder.dtyp:
            if self.initialborder.dtyp.code not in self.ALLOWED_INITBORDER_CODES:
                raise ValidationError({
                    'initialborder': f'فقط محدوده اولیه با کدهای {self.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                })

    def __str__(self):
        return f"آمار عملکرد معادن در حال تجهیز زغال {self.initialborder.title}"
    
    class Meta:
        verbose_name = "آمار عملکرد معادن در حال تجهیز زغال"
        verbose_name_plural = "امارهای عملکرد معادن در حال تجهیز زغال"
        constraints = [
                models.UniqueConstraint(
                    fields=['initialborder','sal', 'doure',], 
                    name='unique_sal_doure_amaramalkardtajhizcoal',
                    violation_error_message='ترکیب سال، دوره قبلاً ثبت شده است.'
                )
            ]


class AmarAmalkardBahrebardariCoal(models.Model):
    ALLOWED_INITBORDER_CODES = [737 , ] # زغال
    
    RAVESH__CHOICES = [(1,'امانی') , (2,'پیمانی یا سرمایه گذار')]
    PEYMANKAR_TYPE_CHOICES = [(1,'حقیقی'),(2,'حقوقی دولتی'),(3,'حقوقی غیر دولتی')]


    initialborder = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="rinitborderamaramalkardbahrebardaricoal",
        blank=False,
        null=False
    )
    sal = models.IntegerField(verbose_name="سال",null=False,blank=False)
    doure = models.IntegerField(verbose_name="دوره",validators=[
            MinValueValidator(1, message="دوره نمی‌تواند کمتر از 1 باشد."),
            MaxValueValidator(12, message="دوره نمی‌تواند بیشتر از 12 باشد.")
        ],null=False,blank=False)
    
    reveshejraamaliyatmadani   = models.IntegerField(verbose_name="روش اجرا عملیات معدنی",choices=RAVESH__CHOICES,blank=True,null=True)
    namepeymankar              = models.CharField(verbose_name="نام پیمانکار/سرمایه گذار",blank=True,null=True)
    peymankar_typ              = models.IntegerField(verbose_name="نوع پیمانکار یا سرمایه گذار",choices=PEYMANKAR_TYPE_CHOICES,blank=True,null=True)
    meghdarestekhraj           = models.FloatField(verbose_name="مقدار استخراج زغالسنگ به تن",blank=True,null=True)
    karkonan_amani_avg         = models.IntegerField(verbose_name="میانگین کارکنان امانی به نفر",null=True,blank=True)
    karkonan_peymani_avg       = models.IntegerField(verbose_name="میانگین کارکنان پیمانی به نفر",null=True,blank=True)
    hajmbatelebardari          = models.FloatField(verbose_name="حجم باطله برداری در معدن روباز به مترمکعب",blank=True,null=True)
    hajmmasrafchoub_avg        = models.FloatField(verbose_name="میانگین مصرف چوب به ازای هر تن تولید در معدن زیرزمینی به کیلوگرم بر تن",blank=True,null=True)
    mavadnarie                 = models.FloatField(verbose_name="مصرف کل مواد ناریه به کیلوگرم",blank=True,null=True)
    masrafab_avg               = models.FloatField(verbose_name="میانگین مصرف آب به ازای هر تن تولید به لیتربرتن",blank=True,null=True)
    masrafbargh_avg            = models.FloatField(verbose_name="میانگین مصرف برق به ازای هر تن به کیلوولت ساعت بر تن",blank=True,null=True)
    masrafsoukht_avg           = models.FloatField(verbose_name="میانگین مصرف سوخت به ازای هر تن به لیتر بر تن",blank=True,null=True)
    zakhireestekhrajbaghimande = models.FloatField(verbose_name="مقدار ذخیره قابل استخراج باقی مانده به هزارتن",blank=True,null=True)
    zakhireamadesazishode      = models.FloatField(verbose_name="مقدار ذخیره آماده سازی شده برای استخراج به هزارتن",blank=True,null=True)
    amouzeshkarkonan           = models.FloatField(verbose_name="آموزس کارکنان به نفردوره",blank=True,null=True)
    mahaltahvilyaforoush       = models.CharField(verbose_name="محل های تحویل یا فروش",max_length=500,blank=True,null=True)

    def clean(self):
        super().clean()
        if self.initialborder and self.initialborder.dtyp:
            if self.initialborder.dtyp.code not in self.ALLOWED_INITBORDER_CODES:
                raise ValidationError({
                    'initialborder': f'فقط محدوده اولیه با کدهای {self.ALLOWED_INITBORDER_CODES} مجاز هستند.'
                })

    def __str__(self):
        return f"آمار عملکرد معادن در حال بهره برداری زغال {self.initialborder.title}"
    
    class Meta:
        verbose_name = "آمار عملکرد معادن در حال بهره برداری زغال"
        verbose_name_plural = "امارهای عملکرد معادن در حال بهره برداری زغال"
        constraints = [
                models.UniqueConstraint(
                    fields=['initialborder','sal', 'doure',], 
                    name='unique_sal_doure_amaramalkardbahrebardaricoal',
                    violation_error_message='ترکیب سال، دوره قبلاً ثبت شده است.'
                )
            ]
