"""
    All InitialBorder Metadata (base on InitialBorderDomin) goes here
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class BaseInitialBorderMetadata(models.Model):
    # All initialborder shenasnameh inherit from this class
    rinitialborder = models.OneToOneField('InitialBorder' , on_delete=models.CASCADE, related_name='%(class)s_rinitialborder') #related_name must be unique
    # this fields are common in all Metadata's
    name        = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    masahat     = models.FloatField(verbose_name="مساحت به کیلومترمربع",unique=False, blank=True, null=True)
    malekiyat   = models.CharField(verbose_name="مالکیت",max_length=100, unique=False, blank=True, null=True)
    ostan       = models.CharField(verbose_name="استان",max_length=100, unique=False, blank=True, null=True)
    shahrestan  = models.CharField(verbose_name="شهرستان",max_length=100, unique=False, blank=True, null=True)

    def __str__(self):
        return f"شناسنامه {self.rinitialborder.title}"

    class Meta:
        abstract = True


class InitialBorderMetadataPahneh(BaseInitialBorderMetadata):
    
    class Meta:
        verbose_name = "شناسنامه محدوده اولیه پهنه"
        verbose_name_plural = "شناسنامه محدوده اولیه پهنه"

class InitialBorderMetadataDarkhastekteshaf(BaseInitialBorderMetadata):
    cadastre      = models.CharField(verbose_name="شماره کاداستر",max_length=100, unique=False, blank=True, null=True)
    noemademadani = models.CharField(verbose_name="نوع ماده معدنی",max_length=100, unique=False, blank=True, null=True)
    organs        = models.CharField(verbose_name="ارگان های استعلام شونده",max_length=250, unique=False, blank=True, null=True)
    
    class Meta:
        verbose_name = "شناسنامه محدوده اولیه درخواست اکتشاف"
        verbose_name_plural = "شناسنامه محدوده اولیه درخواست اکتشاف"

class InitialBorderMetadataParvaneekteshaf(BaseInitialBorderMetadata):
    cadastre        = models.CharField(verbose_name="شماره کاداستر",max_length=100, unique=False, blank=True, null=True)
    noemademadani   = models.CharField(verbose_name="نوع ماده معدنی",max_length=100, unique=False, blank=True, null=True)
    shomareparvaneh = models.CharField(verbose_name="شماره پروانه",max_length=100, unique=False, blank=True, null=True)
    tarikhparvane   = models.DateField(verbose_name="تاریخ پروانه",auto_now=False,auto_now_add=False,null=True,blank=True)
    tarikhetebar    = models.DateField(verbose_name="تاریخ اعتبار",auto_now=False,auto_now_add=False,null=True,blank=True)
    
    class Meta:
        verbose_name = "شناسنامه محدوده اولیه پروانه اکتشاف"
        verbose_name_plural = "شناسنامه محدوده اولیه پروانه اکتشاف"

class InitialBorderMetadataGovahikashf(BaseInitialBorderMetadata):
    cadastre           = models.CharField(verbose_name="شماره کاداستر",max_length=100, unique=False, blank=True, null=True)
    noemademadani      = models.CharField(verbose_name="نوع ماده معدنی",max_length=100, unique=False, blank=True, null=True)
    shomareparvaneh    = models.CharField(verbose_name="شماره پروانه",max_length=100, unique=False, blank=True, null=True)
    tarikhparvane      = models.DateField(verbose_name="تاریخ پروانه",auto_now=False,auto_now_add=False,null=True,blank=True)
    tarietebargovahi   = models.DateField(verbose_name="تاریخ اعتبار گواهی",auto_now=False,auto_now_add=False,null=True,blank=True)
    zakhireehtemali    = models.FloatField(verbose_name="ذخیره احتمالی به تن",unique=False, blank=True, null=True)
    zakhireghatei      = models.FloatField(verbose_name="ذخیره قطعی به تن",unique=False, blank=True, null=True)
    ayarehad           = models.FloatField(verbose_name="عیار حد به درصد",unique=False, blank=True, null=True)
    ayaremeyangin      = models.FloatField(verbose_name="عیار میانگین به درصد",unique=False, blank=True, null=True)
    shomaregovahikashf = models.CharField(verbose_name="شماره گواهی کشف",max_length=100, unique=False, blank=True, null=True)
    tarikhsodurgivahikashf = models.DateField(verbose_name="تاریخ صدور گواهی کشف",auto_now=False,auto_now_add=False,null=True,blank=True)
        
    class Meta:
        verbose_name = "شناسنامه محدوده اولیه گواهی کشف"
        verbose_name_plural = "شناسنامه محدوده اولیه گواهی کشف"

class InitialBorderMetadataParvanebahrebardai(BaseInitialBorderMetadata):
    cadastre          = models.CharField(verbose_name="شماره کاداستر",max_length=100, unique=False, blank=True, null=True)
    noemademadani     = models.CharField(verbose_name="نوع ماده معدنی",max_length=100, unique=False, blank=True, null=True)
    shomareparvaneh   = models.CharField(verbose_name="شماره پروانه",max_length=100, unique=False, blank=True, null=True)
    tarikhparvane     = models.DateField(verbose_name="تاریخ پروانه",auto_now=False,auto_now_add=False,null=True,blank=True)
    tarietebarparvane = models.DateField(verbose_name="تاریخ اعتبار پروانه",auto_now=False,auto_now_add=False,null=True,blank=True)
    zakhireehtemali   = models.FloatField(verbose_name="ذخیره احتمالی به تن",unique=False, blank=True, null=True)
    zakhireghatei     = models.FloatField(verbose_name="ذخیره قطعی به تن",unique=False, blank=True, null=True)
    ayarehad          = models.FloatField(verbose_name="عیار حد به درصد",unique=False, blank=True, null=True)
    ayaremeyangin     = models.FloatField(verbose_name="عیار میانگین به درصد",unique=False, blank=True, null=True)
    estekhrajsaleyane = models.FloatField(verbose_name=" استخراج سالیانه به تن",unique=False, blank=True, null=True)
        
    class Meta:
        verbose_name = "شناسنامه محدوده اولیه پروانه بهره برداری"
        verbose_name_plural = "شناسنامه محدوده اولیه پروانه بهره برداری"

class InitialBorderMetadataPotansielyabi(BaseInitialBorderMetadata):
    noemademadani = models.CharField(verbose_name="نوع ماده معدنی",max_length=100, unique=False, blank=True, null=True)
        
    class Meta:
        verbose_name = "شناسنامه محدوده اولیه پتانسیل یابی"
        verbose_name_plural = "شناسنامه محدوده قانواولیهنی پتانسیل یابی"


class InitialBorderMetadataCoal(BaseInitialBorderMetadata):
    TYPE_CHOICES = [
        (1 , 'کک شو'),
        (2 , 'حرارتی'),
        (3 , 'هردو'),
    ]
    STATUS_CHOICES = [
        (1 , 'درحال بهره برداری'),
        (2 , 'در حال تجهیز'),
        (3 , 'سایر'),
    ]
    typ = models.IntegerField(verbose_name="نوع مصرف اصلی",choices=TYPE_CHOICES,blank=True,null=True)
    status = models.IntegerField(verbose_name="وضعیت معدن",choices=STATUS_CHOICES,blank=True,null=True)

    # Hoghoughi
    BAHREBARDAR_TYPE_CHOICES = [(1,'حقیقی'),(2,'حقوقی دولتی'),(3,'حقوقی غیر دولتی')]
    namebahrebardar                   = models.CharField(verbose_name="نام بهره بردار",blank=True,null=True)
    bahrebardar_typ                   = models.IntegerField(verbose_name="نوع بهره بردار",choices=BAHREBARDAR_TYPE_CHOICES,blank=True,null=True)
    addressmadan                      = models.CharField(verbose_name="آدرس معدن",blank=True,null=True)
    addressdaftar                     = models.CharField(verbose_name="آدرس دفتر",blank=True,null=True)
    shomarecadaster                   = models.CharField(verbose_name="شماره کاداستر",blank=True,null=True)
    shenasemeli                       = models.CharField(verbose_name="شناسه ملی",blank=True,null=True)
    masahat                           = models.FloatField(verbose_name="مساحت",default=0,blank=True,null=True) 
    parvanehekteshaf_shomare          = models.CharField(verbose_name="شماره پروانه اکتشاف",blank=True,null=True)
    parvanehekteshaf_tarikhsodur      = models.DateField(verbose_name="تاریخ صدور پروانه اکتشاف",null=True,blank=True)
    parvanehekteshaf_tatikhengheza    = models.DateField(verbose_name="تاریخ انقضا پروانه اکتشاف",null=True,blank=True)
    govahikashf_shomare               = models.CharField(verbose_name="شماره گواهی کشف",blank=True,null=True)
    govahikashf_tarikhsodure          = models.DateField(verbose_name="تاریخ صدور گواهی کشف",null=True,blank=True)
    parvanebahrebardari_shomare       = models.CharField(verbose_name="شماره پروانه بهره برداری",blank=True,null=True)
    parvanebahrebardari_tarikhsodur   = models.DateField(verbose_name="تاریخ صدور پروانه بهره برداری",null=True,blank=True)
    parvanebahrebardari_tarikhengheza = models.DateField(verbose_name="تاریخ انقضا پروانه بهره برداری",null=True,blank=True)
    
    #Kansar
    mark                              = models.CharField(verbose_name="مارک زغالسنگ (استاندارد روسی)",          blank=True,null=True)
    zarib_pelasto                     = models.FloatField(verbose_name="ضریب پلاستومتری",                         blank=True,null=True)
    tedadlaye                         = models.IntegerField(verbose_name="تعداد لایه ها",                        blank=True,null=True)
    zekhamatlayehayeghabelkar_min     = models.FloatField(verbose_name="ضخامت لایه های قابل کار حداقل",          blank=True,null=True)
    zekhamatlayehayeghabelkar_max     = models.FloatField(verbose_name="ضخامت لایه های قابل کار حداکثر",         blank=True,null=True)
    zekhamatlayehayeghabelkar_avg     = models.FloatField(verbose_name="ضخامت لایه های قابل کار میانگین",        blank=True,null=True)
    shiblaye_min                      = models.FloatField(verbose_name="شیب لایه ها حداقل",                      blank=True,null=True)
    shiblaye_max                      = models.FloatField(verbose_name="شیب لایه ها حداکثر",                     blank=True,null=True)
    shiblaye_avg                      = models.FloatField(verbose_name="شیب لایه ها میانگین",                    blank=True,null=True)
    omghelayehaekteshf_min            = models.FloatField(verbose_name="عمق لایه های اکتشاف شده حداقل",          blank=True,null=True)
    omghelayehaekteshf_max            = models.FloatField(verbose_name="عمق لایه های اکتشاف شده حداکثر",         blank=True,null=True)
    omghelayehaekteshf_avg            = models.FloatField(verbose_name="عمق لایه های اکتشاف شده میانگین",        blank=True,null=True)
    khakestarmatnlayeha_min           = models.FloatField(verbose_name="خاکستر متن لایه های قابل کار حداقل",     blank=True,null=True)
    khakestarmatnlayeha_max           = models.FloatField(verbose_name="خاکستر متن لایه های قابل کار حداکثر",    blank=True,null=True)
    khakestarmatnlayeha_avg           = models.FloatField(verbose_name="خاکستر متن لایه های قابل کار میانگین",   blank=True,null=True)
    rotubatmatnlayeha_min             = models.FloatField(verbose_name="رطوبت متن لایه های قابل کار حداقل",      blank=True,null=True)
    rotubatmatnlayeha_max             = models.FloatField(verbose_name="رطوبت متن لایه های قابل کار حداکثر",     blank=True,null=True)
    rotubatmatnlayeha_avg             = models.FloatField(verbose_name="رطوبت متن لایه های قابل کار میانگین",    blank=True,null=True)
    mohtavagugerdlayeha_min           = models.FloatField(verbose_name="محتوای گوگرد لایه های قابل کار حداقل",   blank=True,null=True)
    mohtavagugerdlayeha_max           = models.FloatField(verbose_name="محتوای گوگرد لایه های قابل کار حداکثر",  blank=True,null=True)
    mohtavagugerdlayeha_avg           = models.FloatField(verbose_name="محتوای گوگرد لایه های قابل کار میانگین", blank=True,null=True)
    arzeshhararatilayeha_min          = models.FloatField(verbose_name="ارزش حرارتی لایه های قابل کار حداقل",    blank=True,null=True)
    arzeshhararatilayeha_max          = models.FloatField(verbose_name="ارزش حرارتی لایه های قابل کار حداکثر",   blank=True,null=True)
    arzeshhararatilayeha_avg          = models.FloatField(verbose_name="ارزش حرارتی لایه های قابل کار میانگین",  blank=True,null=True)
    zakhiretebghegovahikashf_ghati    = models.FloatField(verbose_name="ذخیره طبق گواهی کشف قطعی",       blank=True,null=True)
    zakhiretebghegovahikashf_ehtemali = models.FloatField(verbose_name="ذخیره طبق گواهی کشف احتمالی",    blank=True,null=True)
    zakhiretebghegovahikashf_kol      = models.FloatField(verbose_name="ذخیره طبق گواهی کشف کل",         blank=True,null=True) 
    
    # ParvaneBahrebardari
    RAVESH_ESTEKHRAJ_CHOICES = [
        (1 , 'روباز'),
        (2 , 'زیرزمینی'),
        (3 , 'هردو'),
    ]
    raveshkoliestekhraj          = models.IntegerField(verbose_name="روش کلی استخراج",choices=RAVESH_ESTEKHRAJ_CHOICES,blank=True,null=True)
    bazkonandeasli2             = models.CharField(verbose_name="بازکننده معدن",blank=True,null=True)
    zakhireghabelstekhraj        = models.FloatField(verbose_name="ذخیره قابل استخراج طبق پروانه به هزارتن",blank=True,null=True)
    nesbatzakhireparvenebrgovahi = models.FloatField(verbose_name="نسبت ذخیره قابل استخراج به کل ذخیره طبق گواهی کشف",validators=[
            MinValueValidator(0, message="نسبت ذخیره قابل استخراج به کل ذخیره طبق گواهی کشف نمیتواند کمتر از 0 باشد."),
            MaxValueValidator(100, message="نسبت ذخیره قابل استخراج به کل ذخیره طبق گواهی کشف نمیتواند بیشتر از 100 باشد.")],blank=True,null=True)
    zarfiyatsalane               = models.FloatField(verbose_name="ظرفیت سالانه طبق پروانه به هرازتن",blank=True,null=True)
    modattajhiz_start            = models.IntegerField(verbose_name="سال شروع تجهیز",blank=True,null=True)
    modattajhiz_end              = models.IntegerField(verbose_name="سال پایان تجهیز",blank=True,null=True)
    omrbahrebardari_start        = models.IntegerField(verbose_name="عمر بهره برداری از سال",blank=True,null=True)
    omrbahrebardari_end          = models.IntegerField(verbose_name="عمر بهره برداری تا سال",blank=True,null=True)
    nesbatbatelebekolestekhraj   = models.FloatField(verbose_name="نسبت یاطله کلی به کل ذخیره قابل استخراج",blank=True,null=True)
    omghenahaeiberekhmoon        = models.FloatField(verbose_name="عمق نهایی معدن نسبت به بالاترین سطح رخنمون لایه ها",blank=True,null=True)
    masahattasisatsathi          = models.FloatField(verbose_name="مساحت زیربنای تاسیسات سطحی",blank=True,null=True)
    ehdasvahedkanearaei          = models.BooleanField(verbose_name="احداث واحد کانه آرایی زغالشویی" , default=False) 
    khakestarestekhraji_min      = models.FloatField(verbose_name="خاکستر زغالسنگ استخراجی حداقل",blank=True,null=True)
    khakestarestekhraji_max      = models.FloatField(verbose_name="خاکستر زغالسنگ استخراجی حداکثر",blank=True,null=True)
    khakestarestekhraji_avg      = models.FloatField(verbose_name="خاکستر زغالسنگ استخراجی میانگین",blank=True,null=True)
    khakestarkonsantere          = models.FloatField(verbose_name="خاکستر زغالسنگ کنسانتره",blank=True,null=True)
        
    class Meta:
        verbose_name = "شناسنامه محدوده اولیه زغال "
        verbose_name_plural = "شناسنامه های محدوده اولیه زغال "