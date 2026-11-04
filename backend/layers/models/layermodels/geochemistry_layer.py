from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable

class Anoml_EL_Pg(LinkedToLayerTable):
    ele_name = models.CharField(verbose_name="نام عنصر",max_length=100, unique=False, blank=True, null=True)
    type_smpl = models.CharField(verbose_name="محیط نمونه برداری",max_length=100, unique=False, blank=True, null=True)
    class_el = models.CharField(verbose_name="کلاس",max_length=100, unique=False, blank=True, null=True)
    data_ty = models.CharField(verbose_name="نوع داده",max_length=100, unique=False, blank=True, null=True)
    method = models.CharField(verbose_name="روش تعیین",max_length=100, unique=False, blank=True, null=True)
    upper_lim = models.FloatField(verbose_name="حد بالای آنومالی",unique=False, blank=True, null=True)
    lower_lim = models.FloatField(verbose_name="حد پایین آنومالی",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.ele_name
    class Meta:
        verbose_name = "آنومالی عناصر"
        verbose_name_plural = "آنومالی عناصر"   
        
class Gch_Ano_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    method = models.CharField(verbose_name="روش تعیین",max_length=100, unique=False, blank=True, null=True)
    priority = models.CharField(verbose_name="اولویت",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده اميد بخش ژئوشيمي"
        verbose_name_plural = "محدوده اميد بخش ژئوشيمي"   

class Gch_Lim_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    area = models.FloatField(verbose_name="مساحت محدوده",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده مطالعات ژئوشیمی"
        verbose_name_plural = "محدوده مطالعات ژئوشیمی"           

class Gch_Pt_Sug_Pt(LinkedToLayerTable):
    sampleid = models.CharField(verbose_name="شناسه نمونه",max_length=100, unique=False, blank=True, null=True)
    sampling_ty = models.CharField(verbose_name="روش نمونه برداری",max_length=100, unique=False, blank=True, null=True)
    assay_type = models.CharField(verbose_name="روش آنالیز",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات ",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.sampleid
    class Meta:
        verbose_name = "نقاط پیشنهاد نمونه برداری ژئوشیمیایی"
        verbose_name_plural = "نقاط پیشنهاد نمونه برداری ژئوشیمیایی" 

class Leaching_Pt(LinkedToLayerTable):
    type_m = models.CharField(verbose_name="نام کانی یا فلز",max_length=100, unique=False, blank=True, null=True)
    solvent_ty = models.CharField(verbose_name="نوع حلال",max_length=100, unique=False, blank=True, null=True)
    leach_ty = models.CharField(verbose_name="نوع لیچینگ ",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = "لیچینگ"
        verbose_name_plural = "لیچینگ"   

class I_Cnt_El_Pl(LinkedToLayerTable):
    class_el = models.CharField(verbose_name="کلاس",max_length=100, unique=False, blank=True, null=True)
    data_ty = models.CharField(verbose_name="نوع داده",max_length=100, unique=False, blank=True, null=True)
    method = models.CharField(verbose_name="روش تعیین",max_length=100, unique=False, blank=True, null=True)
    # ele_name = models.FloatField(verbose_name="نام عنصر",unique=False, blank=True, null=True)
    ele_name = models.CharField(verbose_name="نام عنصر",max_length=100, unique=False, blank=True, null=True)
    grade = models.FloatField(verbose_name="میزان عیار",unique=False, blank=True, null=True)
    type_smpl = models.CharField(verbose_name="محیط نمونه برداری",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.clss
    class Meta:
        verbose_name = "منحنی هم عیار عناصر"
        verbose_name_plural = "منحنی هم عیار عناصر"           
                               
class O_Gch_C_Pg(LinkedToLayerTable):
    sampleid = models.CharField(verbose_name="شماره نمونه",max_length=100, unique=False, blank=True, null=True)
    descript = models.CharField(verbose_name="مشخصات نمونه",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.sampleid
    class Meta:
        verbose_name = "سلول برداشت ژئوشیمی"
        verbose_name_plural = "سلول برداشت ژئوشیمی"   
        
class O_Gch_P_Pt(LinkedToLayerTable):
    sampleid = models.CharField(verbose_name="شناسه نمونه",max_length=100, unique=False, blank=True, null=True)
    type_smpl = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    sample_reason = models.CharField(verbose_name="علت نمونه برداری",max_length=100, unique=False, blank=True, null=True)
    smLc_type = models.CharField(verbose_name="نوع نمونه برداري",max_length=100, unique=False, blank=True, null=True)
    test_type = models.CharField(verbose_name="نوع آزمایش",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    
    Aluminum = models.FloatField(verbose_name="ميزان آلومينيوم",unique=False,blank=True,null=True)
    Antimony = models.FloatField(verbose_name="ميزان آنتيموان",unique=False,blank=True,null=True)
    Arsenic = models.FloatField(verbose_name="ميزان آرسنيك",unique=False,blank=True,null=True)
    Barium = models.FloatField(verbose_name="ميزان باريم",unique=False,blank=True,null=True)
    Berylium = models.FloatField(verbose_name="ميزان بريليم",unique=False,blank=True,null=True)
    Bismuth = models.FloatField(verbose_name="ميزان بيسموت",unique=False,blank=True,null=True)
    Boron = models.FloatField(verbose_name="ميزان بر",unique=False,blank=True,null=True)
    Bromine = models.FloatField(verbose_name="ميزان برم",unique=False,blank=True,null=True)
    Cadmium = models.FloatField(verbose_name="ميزان كادميم",unique=False,blank=True,null=True)
    Calcium = models.FloatField(verbose_name="ميزان کلسيم",unique=False,blank=True,null=True)
    Carbon = models.FloatField(verbose_name="ميزان كربن",unique=False,blank=True,null=True)
    Cerium = models.FloatField(verbose_name="ميزان سريم",unique=False,blank=True,null=True)
    Cesium = models.FloatField(verbose_name="ميزان سزيم",unique=False,blank=True,null=True)
    Chlorine = models.FloatField(verbose_name="ميزان كلر",unique=False,blank=True,null=True)
    Chromium = models.FloatField(verbose_name="ميزان كروم",unique=False,blank=True,null=True)
    Cobalt = models.FloatField(verbose_name="ميزان كبالت",unique=False,blank=True,null=True)
    Copper = models.FloatField(verbose_name="ميزان مس",unique=False,blank=True,null=True)
    Dysprosium = models.FloatField(verbose_name="ميزان ديسپروزيم",unique=False,blank=True,null=True)
    Erbium = models.FloatField(verbose_name="ميزان اربيم",unique=False,blank=True,null=True)
    Europium = models.FloatField(verbose_name="ميزان يوروپيم",unique=False,blank=True,null=True)
    Gadolinium = models.FloatField(verbose_name="ميزان گادولينيم",unique=False,blank=True,null=True)
    Gallium = models.FloatField(verbose_name="ميزان گاليم",unique=False,blank=True,null=True)
    Gold = models.FloatField(verbose_name="ميزان طلا",unique=False,blank=True,null=True)
    Hafnium = models.FloatField(verbose_name="ميزان هافنيوم",unique=False,blank=True,null=True)
    Holmium = models.FloatField(verbose_name="ميزان هولميم",unique=False,blank=True,null=True)
    Indium = models.FloatField(verbose_name="ميزان اينديم",unique=False,blank=True,null=True)
    Iridium = models.FloatField(verbose_name="ميزان ايريديم",unique=False,blank=True,null=True)
    Iron = models.FloatField(verbose_name="ميزان آهن",unique=False,blank=True,null=True)
    Lantanum = models.FloatField(verbose_name="ميزان لانتانيم",unique=False,blank=True,null=True)
    Lead = models.FloatField(verbose_name="ميزان سرب",unique=False,blank=True,null=True)
    Lithium = models.FloatField(verbose_name="ميزان ليتيم",unique=False,blank=True,null=True)
    Magnesium = models.FloatField(verbose_name="ميزان منيزيم",unique=False,blank=True,null=True)
    Mangenese = models.FloatField(verbose_name="ميزان منگنز",unique=False,blank=True,null=True)
    Mercury = models.FloatField(verbose_name="ميزان جيوه",unique=False,blank=True,null=True)
    Molybdenum = models.FloatField(verbose_name="ميزان موليبدن",unique=False,blank=True,null=True)
    Neodymium = models.FloatField(verbose_name="ميزان نئوديميوم",unique=False,blank=True,null=True)
    Nickel = models.FloatField(verbose_name="ميزان نيکل",unique=False,blank=True,null=True)
    Niobium = models.FloatField(verbose_name="ميزان نئوبيوم",unique=False,blank=True,null=True)
    Palladium = models.FloatField(verbose_name="ميزان پالاديوم",unique=False,blank=True,null=True)
    Phosphorus = models.FloatField(verbose_name="ميزان فسفر",unique=False,blank=True,null=True)
    Platinum = models.FloatField(verbose_name="ميزان پلاتين",unique=False,blank=True,null=True)
    Potassium = models.FloatField(verbose_name="ميزان پتاسيم",unique=False,blank=True,null=True)
    Praseodymium = models.FloatField(verbose_name="ميزان پرازئوديميم",unique=False,blank=True,null=True)
    Promethium = models.FloatField(verbose_name="ميزان پرومتيم",unique=False,blank=True,null=True)
    Rhenium = models.FloatField(verbose_name="ميزان رينيم",unique=False,blank=True,null=True)
    Rubidium = models.FloatField(verbose_name="ميزان روبيديم",unique=False,blank=True,null=True)
    Samarium = models.FloatField(verbose_name="ميزان ساماريم",unique=False,blank=True,null=True)
    Scandium = models.FloatField(verbose_name="ميزان اسكانديوم",unique=False,blank=True,null=True)
    Selenium = models.FloatField(verbose_name="ميزان سلنيم",unique=False,blank=True,null=True)
    Silver = models.FloatField(verbose_name="ميزان نقره",unique=False,blank=True,null=True)
    Sodium = models.FloatField(verbose_name="ميزان سديم",unique=False,blank=True,null=True)
    Strontium = models.FloatField(verbose_name="ميزان استرانسيم",unique=False,blank=True,null=True)
    Sulfur = models.FloatField(verbose_name="ميزان گوگرد",unique=False,blank=True,null=True)
    Tantalium = models.FloatField(verbose_name="ميزان تانتاليم",unique=False,blank=True,null=True)
    Tellurium = models.FloatField(verbose_name="ميزان تلور",unique=False,blank=True,null=True)
    Terbium = models.FloatField(verbose_name="ميزان تربيم",unique=False,blank=True,null=True)
    Thallium = models.FloatField(verbose_name="ميزان تاليم",unique=False,blank=True,null=True)
    Thorium = models.FloatField(verbose_name="ميزان توريم",unique=False,blank=True,null=True)
    Thulium = models.FloatField(verbose_name="ميزان توليم",unique=False,blank=True,null=True)
    Tin = models.FloatField(verbose_name="ميزان قلع",unique=False,blank=True,null=True)
    Titanuim = models.FloatField(verbose_name="ميزان تيتانيم",unique=False,blank=True,null=True)
    Tungsten = models.FloatField(verbose_name="ميزان تنگستن",unique=False,blank=True,null=True)
    Uranium = models.FloatField(verbose_name="ميزان اورانيوم",unique=False,blank=True,null=True)
    Vanadium = models.FloatField(verbose_name="ميزان واناديم",unique=False,blank=True,null=True)
    Ytterbium = models.FloatField(verbose_name="ميزان ايتربيم",unique=False,blank=True,null=True)
    Ytterium = models.FloatField(verbose_name="ميزان ايتريم",unique=False,blank=True,null=True)
    Zinc = models.FloatField(verbose_name="ميزان روي",unique=False,blank=True,null=True)
    Zirconium = models.FloatField(verbose_name="ميزان زيركونيم",unique=False,blank=True,null=True)
    XRF_SO3 = models.FloatField(verbose_name="سولفور",unique=False,blank=True,null=True)
    XRF_CI = models.FloatField(verbose_name="کلر",unique=False,blank=True,null=True)
    ComplexGeochemicalHalo1 = models.FloatField(verbose_name="ميزان هاله مركب 1",unique=False,blank=True,null=True)
    ComplexGeochemicalHalo2 = models.FloatField(verbose_name="ميزان هاله مركب 2",unique=False,blank=True,null=True)
    ComplexGeochemicalHalo3 = models.FloatField(verbose_name="ميزان هاله مركب 3",unique=False,blank=True,null=True)
    ZonalityCoefficient1 = models.FloatField(verbose_name="ضريب زوناليتي1",unique=False,blank=True,null=True)
    ZonalityCoefficient2 = models.FloatField(verbose_name="ضريب زوناليتي2",unique=False,blank=True,null=True)
    ZonalityCoefficient3 = models.FloatField(verbose_name="ضريب زوناليتي3",unique=False,blank=True,null=True)
    FactorAmount1 = models.FloatField(verbose_name="مقدار فاكتوري 1",unique=False,blank=True,null=True)
    FactorAmount2 = models.FloatField(verbose_name="مقدار فاكتوري 2",unique=False,blank=True,null=True)
    FactorAmount3 = models.FloatField(verbose_name="مقدار فاكتوري 3",unique=False,blank=True,null=True)
    FactorAmount4 = models.FloatField(verbose_name="مقدار فاكتوري 4",unique=False,blank=True,null=True)
    FactorAmount5 = models.FloatField(verbose_name="مقدار فاكتوري 5",unique=False,blank=True,null=True)
    FactorAmount6 = models.FloatField(verbose_name="مقدار فاكتوري 6",unique=False,blank=True,null=True)
    FactorAmount7 = models.FloatField(verbose_name="مقدار فاكتوري 7",unique=False,blank=True,null=True)
    FactorAmount8 = models.FloatField(verbose_name="مقدار فاكتوري 8",unique=False,blank=True,null=True)
    FactorAmount9 = models.FloatField(verbose_name="مقدار فاكتوري 9",unique=False,blank=True,null=True)
    FactorAmount10 = models.FloatField(verbose_name="مقدار فاكتوري 10",unique=False,blank=True,null=True)
    XRF_LOI = models.FloatField(verbose_name="مواد فرار",unique=False,blank=True,null=True)
    XRF_SiO2 = models.FloatField(verbose_name="اکسيد سيليس",unique=False,blank=True,null=True)
    XRF_Al2O3 = models.FloatField(verbose_name="اکسيد آلومينيوم",unique=False,blank=True,null=True)
    XRF_Fe2O3 = models.FloatField(verbose_name="اکسيد آهن",unique=False,blank=True,null=True)
    XRF_CaO = models.FloatField(verbose_name="اکسيد کلسيم",unique=False,blank=True,null=True)
    XRF_K2O = models.FloatField(verbose_name="اکسيد پتاسيم",unique=False,blank=True,null=True)
    XRF_MgO = models.FloatField(verbose_name="اکسيد منيزيم",unique=False,blank=True,null=True)
    XRF_Na2O = models.FloatField(verbose_name="اکسيد سديم",unique=False,blank=True,null=True)
    XRF_MnO = models.FloatField(verbose_name="اکسيد منگنز",unique=False,blank=True,null=True)
    XRF_TiO2 = models.FloatField(verbose_name="اکسيد تيتان",unique=False,blank=True,null=True)
    XRF_P2O5 = models.FloatField(verbose_name="اکسيد فسفر",unique=False,blank=True,null=True)
    XRF_SrO = models.FloatField(verbose_name="اکسيد استرانسيوم",unique=False,blank=True,null=True)
    XRF_Cr2O3 = models.FloatField(verbose_name="اکسيد کروم",unique=False,blank=True,null=True)
    XRF_NiO = models.FloatField(verbose_name="اکسيد نيکل",unique=False,blank=True,null=True)
    XRF_ZnO = models.FloatField(verbose_name="اکسيد روي",unique=False,blank=True,null=True)
    XRF_V2O5 = models.FloatField(verbose_name="اکسيد واناديم",unique=False,blank=True,null=True)
    XRF_CuO = models.FloatField(verbose_name="اکسيد مس",unique=False,blank=True,null=True)
    XRF_FeO = models.FloatField(verbose_name="اکسيد آهن_دوظرفيتي",unique=False,blank=True,null=True)
    XRF_PbO = models.FloatField(verbose_name="اکسید سرب",unique=False,blank=True,null=True)
 
    
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.sampleid
    class Meta:
        verbose_name = "نقطه برداشت ژئوشیمی"
        verbose_name_plural = "نقطه برداشت ژئوشیمی"           
        
class Hydro_Gch_Pt_Pt(LinkedToLayerTable):
    sampleid = models.CharField(verbose_name="شماره نمونه",max_length=100, unique=False, blank=True, null=True)
    ph = models.FloatField(verbose_name="اسیدیته",unique=False, blank=True, null=True)
    eh = models.FloatField(verbose_name="پتانسيل الکتريکي",unique=False, blank=True, null=True)
    do = models.FloatField(verbose_name="اکسيژن محلول",unique=False, blank=True, null=True)
    temp = models.FloatField(verbose_name="دما",unique=False, blank=True, null=True)
    ec = models.FloatField(verbose_name="هدايت الکتريکي",unique=False, blank=True, null=True)
    tds = models.FloatField(verbose_name="کل مواد جامد محلول",unique=False, blank=True, null=True)
    ts = models.FloatField(verbose_name="کل مواد جامد معلق",unique=False, blank=True, null=True)
    tss= models.FloatField(verbose_name="کل مواد جامد محلول و معلق",unique=False, blank=True, null=True)
    turbidity = models.FloatField(verbose_name="آشفتگي",unique=False, blank=True, null=True)
    salinity = models.FloatField(verbose_name="شوری",unique=False, blank=True, null=True)
    alkal = models.FloatField(verbose_name="قليايي",unique=False, blank=True, null=True)
    clm = models.FloatField(verbose_name="کلريد",unique=False, blank=True, null=True)
    so4m = models.FloatField(verbose_name="سولفات",unique=False, blank=True, null=True)
    hco3m = models.FloatField(verbose_name="بي کربنات",unique=False, blank=True, null=True)
    co3m2 = models.FloatField(verbose_name="کربنات",unique=False, blank=True, null=True)
    so3m2 = models.FloatField(verbose_name="سولفيد",unique=False, blank=True, null=True)
    no3m = models.FloatField(verbose_name="نيترات",unique=False, blank=True, null=True)
    fm = models.FloatField(verbose_name="فلوريد",unique=False, blank=True, null=True)
    po4m = models.FloatField(verbose_name="فسفات",unique=False, blank=True, null=True)
    no2m = models.FloatField(verbose_name="نیتریت",unique=False, blank=True, null=True)
    nh3 = models.FloatField(verbose_name="آمونیاک",unique=False, blank=True, null=True)
    cap2 = models.FloatField(verbose_name="کلسیم",unique=False, blank=True, null=True)
    mgp2 = models.FloatField(verbose_name="منیزیم",unique=False, blank=True, null=True)
    nap = models.FloatField(verbose_name="سدیم",unique=False, blank=True, null=True)
    si = models.FloatField(verbose_name="سیلیس",unique=False, blank=True, null=True)
    brm = models.FloatField(verbose_name="برمید",unique=False, blank=True, null=True)
    b = models.FloatField(verbose_name="بور",unique=False, blank=True, null=True)
    fe = models.FloatField(verbose_name="آهن",unique=False, blank=True, null=True)
    kp = models.FloatField(verbose_name="پتاسیم",unique=False, blank=True, null=True)
    cn = models.FloatField(verbose_name="سیانید",unique=False, blank=True, null=True)
    sm2 = models.FloatField(verbose_name="سولفید",unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.sampleid
    class Meta:
        verbose_name = "نقاط نمونه برداری هیدروژئوشیمی"
        verbose_name_plural = "نقاط نمونه برداری هیدروژئوشیمی"  
       
class O_H_Mnl_P_Pt(LinkedToLayerTable):
    sampleid = models.CharField(verbose_name="شماره نمونه",max_length=100, unique=False, blank=True, null=True)
    amphibol = models.FloatField(verbose_name="آمفیبول",unique=False, blank=True, null=True)
    anatase = models.FloatField(verbose_name="آناتاز",unique=False, blank=True, null=True)
    apatite = models.FloatField(verbose_name="آپاتیت",unique=False, blank=True, null=True)
    barite = models.FloatField(verbose_name="باریت",unique=False, blank=True, null=True)
    biotite = models.FloatField(verbose_name="بیوتیت",unique=False, blank=True, null=True)
    calcite = models.FloatField(verbose_name="کلسیت",unique=False, blank=True, null=True)
    celestine = models.FloatField(verbose_name="سلستین",unique=False, blank=True, null=True)
    cholorite = models.FloatField(verbose_name="کلریت",unique=False, blank=True, null=True)
    chromite = models.FloatField(verbose_name="کرومیت",unique=False, blank=True, null=True)
    cinnabar = models.FloatField(verbose_name="سینابر",unique=False, blank=True, null=True)
    epidots = models.FloatField(verbose_name="اپیدوت",unique=False, blank=True, null=True)
    feldespar = models.FloatField(verbose_name="فلدسپار",unique=False, blank=True, null=True)
    galena = models.FloatField(verbose_name="گالن",unique=False, blank=True, null=True)
    garnet = models.FloatField(verbose_name="گارنت",unique=False, blank=True, null=True)
    geothite = models.FloatField(verbose_name="ژئوتیت",unique=False, blank=True, null=True)
    gold = models.FloatField(verbose_name="طلا",unique=False, blank=True, null=True)
    hematite = models.FloatField(verbose_name="هماتیت",unique=False, blank=True, null=True)
    ilmenite = models.FloatField(verbose_name="ایلمنیت",unique=False, blank=True, null=True)
    leucoxene = models.FloatField(verbose_name="لوکوکسن",unique=False, blank=True, null=True)
    magnetite = models.FloatField(verbose_name="مگنتیت",unique=False, blank=True, null=True)
    n_copper = models.FloatField(verbose_name="مس آزاد",unique=False, blank=True, null=True)
    n_lead = models.FloatField(verbose_name="سرب آزاد",unique=False, blank=True, null=True)
    pyrite_ox = models.FloatField(verbose_name="پیریت (اکسید)",unique=False, blank=True, null=True)
    pyrolusite = models.FloatField(verbose_name="پیرولوسیت",unique=False, blank=True, null=True)
    pyroxenes = models.FloatField(verbose_name="پیروکسن",unique=False, blank=True, null=True)
    rutile = models.FloatField(verbose_name="روتیل",unique=False, blank=True, null=True)
    scheelite = models.FloatField(verbose_name="شئلیت",unique=False, blank=True, null=True)
    serpentin = models.FloatField(verbose_name="سرپانتین",unique=False, blank=True, null=True)
    zircon = models.FloatField(verbose_name="زیرکن",unique=False, blank=True, null=True)
    malachite = models.FloatField(verbose_name="مالاکیت",unique=False, blank=True, null=True)
    silicate_alt = models.FloatField(verbose_name="سیلیکات های آلتره",unique=False, blank=True, null=True)
    chrysocolla = models.FloatField(verbose_name="کریزوکلا",unique=False, blank=True, null=True)
    jarosite = models.FloatField(verbose_name="ژاروسیت",unique=False, blank=True, null=True)
    pb_sec_min = models.FloatField(verbose_name="کانی های ثانویه سرب",unique=False, blank=True, null=True)
    zn_sec_min = models.FloatField(verbose_name="کانی های ثانویه روی",unique=False, blank=True, null=True)
    pyrite = models.FloatField(verbose_name="پیریت",unique=False, blank=True, null=True)
    pyrite_Limonite = models.FloatField(verbose_name="پیریت-لیمونیت",unique=False, blank=True, null=True)
    fe_minerals = models.FloatField(verbose_name="کانیهای آهن دار",unique=False, blank=True, null=True)
    ti_minerals = models.FloatField(verbose_name="کانیهای تیتان دار",unique=False, blank=True, null=True)
    ologist = models.FloatField(verbose_name="اولیژیست",unique=False, blank=True, null=True)
    epidot_chl = models.FloatField(verbose_name="اپیدوت- کلریت",unique=False, blank=True, null=True)
    ologist = models.FloatField(verbose_name="اولیژیست",unique=False, blank=True, null=True)
    altered_minerals = models.FloatField(verbose_name="کانی دگرسان شده",unique=False, blank=True, null=True)
    chalcopyrite = models.FloatField(verbose_name="کالکوپیریت",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.sampleid
    class Meta:
        verbose_name = "نقطه برداشت کانی سنگین"
        verbose_name_plural = "نقطه برداشت کانی سنگین"  

class U_Drg_Z_Pg(LinkedToLayerTable):
    sampleid = models.CharField(verbose_name="شماره نمونه (کانی سنگین یا نمونه ژئوشیمی)",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.sampleid
    class Meta:
        verbose_name = "حوضه آبریز بالا دست"
        verbose_name_plural = "حوضه آبریز بالا دست"