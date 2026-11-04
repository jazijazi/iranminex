from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable

class Alteration_Area_Pg(LinkedToLayerTable):
    alt_name = models.CharField(verbose_name="نام دگرسانی",max_length=100, unique=False, blank=True, null=True)
    comment_fa = models.CharField(verbose_name="توضیحات فارسی",max_length=250, unique=False, blank=True, null=True)
    comment_en = models.CharField(verbose_name="توضیحات لاتین",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.alt_name
    class Meta:
        verbose_name = "محدوده دگرسان شده"
        verbose_name_plural = "محدوده دگرسان شده"  
        
class Caldera_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کالدرا"
        verbose_name_plural = "کالدرا"   

class Dike_Pl_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    structure = models.CharField(verbose_name="نوع ساخت",max_length=100, unique=False, blank=True, null=True)
    texture = models.CharField(verbose_name="نوع بافت",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دایک"
        verbose_name_plural = "دایک"  
        
class Dike_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    structure = models.CharField(verbose_name="نوع ساخت",max_length=100, unique=False, blank=True, null=True)
    texture = models.CharField(verbose_name="نوع بافت",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دایک"
        verbose_name_plural = "دایک"          
       
class Fault_Geology_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام گسل",max_length=100, unique=False, blank=True, null=True)
    type_fault = models.CharField(verbose_name="نوع گسل",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد-آزیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direct = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "گسل زمین شناسی"
        verbose_name_plural = "گسل زمین شناسی"   
       
class Fault_Zone_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام گسل",max_length=100, unique=False, blank=True, null=True)
    type_f = models.CharField(verbose_name="نوع گسل",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زون گسلیدگی"
        verbose_name_plural = "زون گسلیدگی"  

class Fold_Ax_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    fld_ty_maj = models.CharField(verbose_name="نوع اصلی",max_length=100, unique=False, blank=True, null=True)
    old_ty_min = models.CharField(verbose_name="نوع فرعی",max_length=100, unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد محور",unique=False, blank=True, null=True)
    plang_ax = models.FloatField(verbose_name="پلانژ محور",unique=False, blank=True, null=True)
    fold_con = models.CharField(verbose_name="وضعیت چین",max_length=100, unique=False, blank=True, null=True)
    fold_mech = models.CharField(verbose_name="مکانیزم چین خوردگی",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محور چین خوردگی"
        verbose_name_plural = "محور چین خوردگی" 
        
class Fossil_Pt(LinkedToLayerTable):
    fossil_ty = models.CharField(verbose_name="نوع فسیل",max_length=100, unique=False, blank=True, null=True)
    fossil_na = models.CharField(verbose_name="نام فسیل",max_length=100, unique=False, blank=True, null=True)
    sedim_env = models.CharField(verbose_name="محیط رسوب گذاری",max_length=100, unique=False, blank=True, null=True)
    era = models.CharField(verbose_name="سن دوران",max_length=100, unique=False, blank=True, null=True)
    period = models.CharField(verbose_name="سن دوره",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.fossil_ty
    class Meta:
        verbose_name = "فسیل"
        verbose_name_plural = "فسیل"  

class Glg_Lim_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده مطالعات زمین شناسی"
        verbose_name_plural = "محدوده مطالعات زمین شناسی"        

class Glg_Sec_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد (آزیموت)",unique=False, blank=True, null=True)
    end_x_coor = models.FloatField(verbose_name="مختصات X انتها",unique=False, blank=True, null=True)
    end_y_coor = models.FloatField(verbose_name="مختصاتY انتها",unique=False, blank=True, null=True)
    start_x_coor = models.FloatField(verbose_name="مختصات Xابتدا",unique=False, blank=True, null=True)
    start_y_coor = models.FloatField(verbose_name="مختصاتY ابتدا",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مقطع زمین شناسی"
        verbose_name_plural = "مقطع زمین شناسی"                

class Glg_Smpl_Lc_Pt(LinkedToLayerTable):
    sampleid = models.CharField(verbose_name="شماره نمونه",max_length=100, unique=False, blank=True, null=True)
    smlc_type = models.CharField(verbose_name="نوع نمونه برداري",max_length=100, unique=False, blank=True, null=True)
    specif_type = models.CharField(verbose_name="مشخصات نمونه",max_length=250, unique=False, blank=True, null=True)
    test_type = models.CharField(verbose_name="نوع آزمايش",max_length=100, unique=False, blank=True, null=True)
    sampl_res = models.CharField(verbose_name="نتايج مطالعات نمونه برداري",max_length=100, unique=False, blank=True, null=True)
    
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
        verbose_name = "محل نمونه برداری زمین شناسی"
        verbose_name_plural = "محل نمونه برداری زمین شناسی"
        
class Gossan_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    gossan_ty = models.CharField(verbose_name="نوع گوسان",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "گوسان"
        verbose_name_plural = "گوسان"    

class Gossan_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    gossan_ty = models.CharField(verbose_name="نوع گوسان",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "گوسان"
        verbose_name_plural = "گوسان"  
        
class GPS_Track_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام مسیر",max_length=100, unique=False, blank=True, null=True)
    expertname = models.CharField(verbose_name="نام کارشناس",max_length=100, unique=False, blank=True, null=True)
    survey_stage = models.CharField(verbose_name="مرحله پيمايش",max_length=100, unique=False, blank=True, null=True)
    date = models.DateField(verbose_name="تاریخ",auto_now=False,auto_now_add=False,null=True,blank=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مسیر پیمایش"
        verbose_name_plural = "مسیر پیمایش"

class GPS_Track_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام مسیر",max_length=100, unique=False, blank=True, null=True)
    expertname = models.CharField(verbose_name="نام کارشناس",max_length=100, unique=False, blank=True, null=True)
    survey_stage = models.CharField(verbose_name="مرحله پيمايش",max_length=100, unique=False, blank=True, null=True)
    date = models.DateField(verbose_name="تاریخ",auto_now=False,auto_now_add=False,null=True,blank=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مسیر پیمایش"
        verbose_name_plural = "مسیر پیمایش"

class Profile_Pl(LinkedToLayerTable):
    #deleted from layer names
    name = models.CharField(verbose_name="نام مسیر",max_length=100, unique=False, blank=True, null=True)
    expertname = models.CharField(verbose_name="نام کارشناس",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پروفیل"
        verbose_name_plural = "پروفیل"       

class Land_Sld_Pg(LinkedToLayerTable):
    material_ty = models.CharField(verbose_name="نوع مواد دربرگیرنده",max_length=100, unique=False, blank=True, null=True)
    move_ty = models.CharField(verbose_name="نوع حرکت",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.material_ty
    class Meta:
        verbose_name = "زمین لغزش"
        verbose_name_plural = "زمین لغزش"    

class Linear_Pl(LinkedToLayerTable):
    name_en = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "عوارض خطی"
        verbose_name_plural = "عوارض خطی"  

class Ore_Location_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    mineral_ty = models.CharField(verbose_name="نوع ماده معدنی",max_length=100, unique=False, blank=True, null=True)
    x = models.FloatField(verbose_name="Xمختصات ",unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="Yمختصات",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محل ماده معدنی "
        verbose_name_plural = "محل ماده معدنی "
        
class Str_D_M_Pt(LinkedToLayerTable):
    dip_direc = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد-ازیموت",unique=False, blank=True, null=True)
    type_str = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.dip_direc
    class Meta:
        verbose_name = "محل اندازه گیری شیب و امتداد"
        verbose_name_plural = "محل اندازه گیری شیب و امتداد"
 
class Mn_Indc_Location_Pt(LinkedToLayerTable):
    abbrevname = models.CharField(verbose_name="نام کانه یا عنصر به اختصار",max_length=100, unique=False, blank=True, null=True)
    min_ty = models.CharField(verbose_name="تیپ کانی سازی",max_length=100, unique=False, blank=True, null=True)
    host_ty = models.CharField(verbose_name="سنگ میزبان",max_length=100, unique=False, blank=True, null=True)
    indic_ty = models.CharField(verbose_name="نوع نشانه",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.abbrevname
    class Meta:
        verbose_name = "محل نشانه کانه زایی"
        verbose_name_plural = "محل نشانه کانه زایی" 
               
class Mnr_Ocr_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره محدوده",max_length=100, unique=False, blank=True, null=True)
    ore_occ_sh = models.CharField(verbose_name="شکل تجمع",max_length=100, unique=False, blank=True, null=True)
    zone_ty = models.CharField(verbose_name="نوع وزن",max_length=100, unique=False, blank=True, null=True)
    mineral_ty = models.CharField(verbose_name="نوع کانی",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده کانی سازی"
        verbose_name_plural = "محدوده کانی سازی"   

class Mine_Dump_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    ore_type = models.CharField(verbose_name="نوع ماده معدني",max_length=100, unique=False, blank=True, null=True)
    mine_name = models.CharField(verbose_name="نام معدن (محدوده)",max_length=100, unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم ماده معدنی",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دامپ معدنی"
        verbose_name_plural = "دامپ معدنی"    

class Mine_Dump_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    ore_type = models.CharField(verbose_name="نوع ماده معدني",max_length=100, unique=False, blank=True, null=True)
    mine_name = models.CharField(verbose_name="نام معدن (محدوده)",max_length=100, unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم ماده معدنی",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دامپ معدنی"
        verbose_name_plural = "دامپ معدنی"

class Mine_Dump_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    ore_type = models.CharField(verbose_name="نوع ماده معدني",max_length=100, unique=False, blank=True, null=True)
    mine_name = models.CharField(verbose_name="نام معدن (محدوده)",max_length=100, unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم ماده معدنی",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دامپ معدنی"
        verbose_name_plural = "دامپ معدنی"     
        
class Mine_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام معدن",max_length=100, unique=False, blank=True, null=True)
    mine_ty = models.CharField(verbose_name="نوع معدنکاری",max_length=100, unique=False, blank=True, null=True)
    ope_condit = models.CharField(verbose_name="وضعیت فعالیت",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "معدن"
        verbose_name_plural = "معدن"    

class Mine_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام معدن",max_length=100, unique=False, blank=True, null=True)
    mine_ty = models.CharField(verbose_name="نوع معدنکاری",max_length=100, unique=False, blank=True, null=True)
    ope_condit = models.CharField(verbose_name="وضعیت فعالیت",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "معدن"
        verbose_name_plural = "معدن"         
                
class Pro_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    depositetype = models.CharField(verbose_name="نوع ذخیره",max_length=100, unique=False, blank=True, null=True)
    priority = models.CharField(verbose_name="اولویت",max_length=100, unique=False, blank=True, null=True)
    det_method = models.CharField(verbose_name="روش تعیین ذخیره",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده پیشنهادی"
        verbose_name_plural = "محدوده پیشنهادی"  
        
class Rck_Typ_Leg_Pg(LinkedToLayerTable):
    geo_unit = models.CharField(verbose_name="نام لایه به اختصار",max_length=100, unique=False, blank=True, null=True)
    formation = models.CharField(verbose_name="سازند",max_length=100, unique=False, blank=True, null=True)
    era = models.CharField(verbose_name="دوران",max_length=100, unique=False, blank=True, null=True)
    period = models.CharField(verbose_name="دوره",max_length=100, unique=False, blank=True, null=True)
    origin = models.CharField(verbose_name="خاستگاه",max_length=100, unique=False, blank=True, null=True)
    comment_en = models.CharField(verbose_name="توضیحات انگلیسی",max_length=250, unique=False, blank=True, null=True)
    comment_fa = models.CharField(verbose_name="توضیحات فارسی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.geo_unit
    class Meta:
        verbose_name = "راهنمای تیپ سنگ شناسی"
        verbose_name_plural = "راهنمای تیپ سنگ شناسی"
        
class Rck_Typ_Leg_Pl(LinkedToLayerTable):
    geo_unit = models.CharField(verbose_name="نام لایه به اختصار",max_length=100, unique=False, blank=True, null=True)
    formation = models.CharField(verbose_name="سازند",max_length=100, unique=False, blank=True, null=True)
    era = models.CharField(verbose_name="دوران",max_length=100, unique=False, blank=True, null=True)
    period = models.CharField(verbose_name="دوره",max_length=100, unique=False, blank=True, null=True)
    origin = models.CharField(verbose_name="خاستگاه",max_length=100, unique=False, blank=True, null=True)
    comment_en = models.CharField(verbose_name="توضیحات انگلیسی",max_length=250, unique=False, blank=True, null=True)
    comment_fa = models.CharField(verbose_name="توضیحات فارسی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.geo_unit
    class Meta:
        verbose_name = "راهنمای تیپ سنگ شناسی"
        verbose_name_plural = "راهنمای تیپ سنگ شناسی"        

class Rck_Typ_Area_Pg(LinkedToLayerTable):
    geo_unit = models.CharField(verbose_name="نام لایه به اختصار",max_length=100, unique=False, blank=True, null=True)
    lable = models.CharField(verbose_name="کد واحد سنگی",max_length=100, unique=False, blank=True, null=True)
    formation = models.CharField(verbose_name="سازند",max_length=100, unique=False, blank=True, null=True)
    era = models.CharField(verbose_name="دوران",max_length=100, unique=False, blank=True, null=True)
    period = models.CharField(verbose_name="دوره",max_length=100, unique=False, blank=True, null=True)
    origin = models.CharField(verbose_name="خاستگاه",max_length=100, unique=False, blank=True, null=True)
    structure = models.CharField(verbose_name="نوع ساخت",max_length=100, unique=False, blank=True, null=True)
    format_bo = models.CharField(verbose_name="نوع توده",max_length=100, unique=False, blank=True, null=True)
    complx = models.CharField(verbose_name="نام کمپلکس",max_length=100, unique=False, blank=True, null=True)
    series = models.CharField(verbose_name="نام سری",max_length=100, unique=False, blank=True, null=True)
    texture = models.CharField(verbose_name="نوع بافت",max_length=100, unique=False, blank=True, null=True)
    comment_en = models.CharField(verbose_name="توضیحات انگلیسی",max_length=250, unique=False, blank=True, null=True)
    comment_fa = models.CharField(verbose_name="توضیحات فارسی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.geo_unit
    class Meta:
        verbose_name = "تیپ سنگ شناسی"
        verbose_name_plural = "تیپ سنگ شناسی"
        
class Unit_Bound_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    contact = models.CharField(verbose_name="وضعیت همبری",max_length=100, unique=False, blank=True, null=True)
    contact_ty = models.CharField(verbose_name="نوع همبری",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "همبری واحدها"
        verbose_name_plural = "همبری واحدها" 
      
class Struct_Zone_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زون ساختاری"
        verbose_name_plural = "زون ساختاری"
        
class Slag_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سرباره"
        verbose_name_plural = "سرباره"
 
class Slag_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="نام یا شماره",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سرباره"
        verbose_name_plural = "سرباره"  

class Vein_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    mnrl_cond = models.CharField(verbose_name="وضعیت کانی‌سازی",max_length=100, unique=False, blank=True, null=True)
    vein_condition = models.CharField(verbose_name="وضعیت رگه",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    m_thicknes = models.FloatField(verbose_name="ضخامت متوسط",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "رگه"
        verbose_name_plural = "رگه"
        
class Vein_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    mnrl_cond = models.CharField(verbose_name="وضعیت کانی‌سازی",max_length=100, unique=False, blank=True, null=True)
    vein_condition = models.CharField(verbose_name="وضعیت رگه",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    m_thicknes = models.FloatField(verbose_name="ضخامت متوسط",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "رگه"
        verbose_name_plural = "رگه"
        
class Vein_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    mnrl_cond = models.CharField(verbose_name="وضعیت کانی‌سازی",max_length=100, unique=False, blank=True, null=True)
    vein_condition = models.CharField(verbose_name="وضعیت رگه",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    m_thicknes = models.FloatField(verbose_name="ضخامت متوسط",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "رگه"
        verbose_name_plural = "رگه"

class Min_Trn_Pg(LinkedToLayerTable):
    trench_no = models.CharField(verbose_name="شناسه ترانشه",max_length=100, unique=False, blank=True, null=True)
    wt_type = models.CharField(verbose_name="نوع ترانشه",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.trench_no
    class Meta:
        verbose_name = "ترانشه معدنی"
        verbose_name_plural = "ترانشه معدنی"  

class Min_Trn_Pt(LinkedToLayerTable):
    trench_no = models.CharField(verbose_name="شناسه ترانشه",max_length=100, unique=False, blank=True, null=True)
    wt_type = models.CharField(verbose_name="نوع ترانشه",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.trench_no
    class Meta:
        verbose_name = "ترانشه معدنی"
        verbose_name_plural = "ترانشه معدنی"  

class Min_Trn_Pl(LinkedToLayerTable):
    trench_no = models.CharField(verbose_name="شناسه ترانشه",max_length=100, unique=False, blank=True, null=True)
    wt_type = models.CharField(verbose_name="نوع ترانشه",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.trench_no
    class Meta:
        verbose_name = "ترانشه معدنی"
        verbose_name_plural = "ترانشه معدنی"

class Old_Work_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کار قدیمی"
        verbose_name_plural = "کار قدیمی"

class Old_Work_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کار قدیمی"
        verbose_name_plural = "کار قدیمی"

class Joint_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد آزیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "درزه"
        verbose_name_plural = "درزه"

class Glg_Sec_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد (آزیموت)",unique=False, blank=True, null=True)
    end_x_coor = models.FloatField(verbose_name="مختصات X انتها",unique=False, blank=True, null=True)
    end_y_coor = models.FloatField(verbose_name="مختصاتY انتها",unique=False, blank=True, null=True)
    start_x_coor = models.FloatField(verbose_name="مختصات Xابتدا",unique=False, blank=True, null=True)
    start_y_coor = models.FloatField(verbose_name="مختصاتY ابتدا",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مقطع زمین شناسی"
        verbose_name_plural = "مقطع زمین شناسی"   

class Glg_P_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پروفیل پیمایش"
        verbose_name_plural = "پروفیل پیمایش" 

class Glg_Ano_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comp_st = models.CharField(verbose_name="نوع مطالعه تکمیلی",max_length=100, unique=False, blank=True, null=True)
    priority = models.CharField(verbose_name="اولویت",max_length=100, unique=False, blank=True, null=True)
    deposite_type = models.CharField(verbose_name="تیپ ذخیره",max_length=100, unique=False, blank=True, null=True)
    method = models.CharField(verbose_name="روش تعیین",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده پیشنهادی زمین شناسی"
        verbose_name_plural = "محدوده پیشنهادی زمین شناسی" 