from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable


class Coal_Ano_Pg(LinkedToLayerTable):
    typ_coal = models.CharField(verbose_name=" نوع زغال",max_length=100, unique=False, blank=True, null=True)
    down_lim = models.FloatField(verbose_name="حدپایین",unique=False, blank=True, null=True)
    up_lim = models.FloatField(verbose_name="حدبالا",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.typ
    class Meta:
        verbose_name = "محدوده ناهنجاری زغال"
        verbose_name_plural = "محدوده ناهنجاری زغال"
        
class Coal_Isoline_Pl(LinkedToLayerTable):  
    type_Iso = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    value = models.FloatField(verbose_name="مقدار",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.depth_ele
    class Meta:
        verbose_name = "منحنی هم میزان زغال"
        verbose_name_plural = "منحنی هم میزان زغال"  
        
class Coal_Block_Pg(LinkedToLayerTable):
    name_b = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    catagory = models.CharField(verbose_name="رده بندی",max_length=100, unique=False, blank=True, null=True)
    density_av = models.FloatField(verbose_name="متوسط وزن مخصوص",unique=False, blank=True, null=True)
    dip_av = models.FloatField(verbose_name="متوسط شیب",unique=False, blank=True, null=True)
    reserve = models.FloatField(verbose_name="تناژ ذخیره",unique=False, blank=True, null=True)
    thick_av = models.FloatField(verbose_name="متوسط ضخامت",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.catagory
    class Meta:
        verbose_name = "بلوک بندی زغال"
        verbose_name_plural = "بلوک بندی زغال"     

class Coal_La_Pg(LinkedToLayerTable):
    coal_lim = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True) 
    abbrev = models.CharField(verbose_name="علامت اختصاری",max_length=100, unique=False, blank=True, null=True)
    coal_mark = models.CharField(verbose_name="مارک زغال",max_length=100, unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    strik = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    dip_direc = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    lav_thicknes = models.FloatField(verbose_name="ضخامت متوسط",unique=False, blank=True, null=True)
    maseral_type = models.CharField(verbose_name="نوع ماسرال",max_length=100, unique=False, blank=True, null=True)
    work_ab = models.CharField(verbose_name="قابلیت کار",max_length=100, unique=False, blank=True, null=True)
    key_bed = models.CharField(verbose_name="لایه راهنما",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.coal_lim 
    class Meta:
        verbose_name = "لایه زغال "
        verbose_name_plural = "لایه زغال "       

class Coal_La_Pl(LinkedToLayerTable):
    coal_lim = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True) 
    abbrev = models.CharField(verbose_name="علامت اختصاری",max_length=100, unique=False, blank=True, null=True)
    coal_mark = models.CharField(verbose_name="مارک زغال",max_length=100, unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    strik = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    dip_direc = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    lav_thicknes = models.FloatField(verbose_name="ضخامت متوسط",unique=False, blank=True, null=True)
    maseral_type = models.CharField(verbose_name="نوع ماسرال",max_length=100, unique=False, blank=True, null=True)
    work_ab = models.CharField(verbose_name="قابلیت کار",max_length=100, unique=False, blank=True, null=True)
    key_bed = models.CharField(verbose_name="لایه راهنما",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.coal_lim 
    class Meta:
        verbose_name = "لایه زغال "
        verbose_name_plural = "لایه زغال "    
        
class Coal_Lim_Pg(LinkedToLayerTable):
    coal_lim = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.coal_lim 
    class Meta:
        verbose_name = "محدوده مطالعات زغال"
        verbose_name_plural = "محدوده مطالعات زغال"    
        
class Coal_Mark_M_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    coal_mark = models.CharField(verbose_name="مارک زغال",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = "نقشه مارک زغال"
        verbose_name_plural = "نقشه مارک زغال"            
               
class Co_Min_Trn_Pg(LinkedToLayerTable):
    coal_lim = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    trench_no = models.CharField(verbose_name="نام یا شماره ترانشه",max_length=100, unique=False, blank=True, null=True)
    type_trn = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد (آزیموت)",unique=False, blank=True, null=True)
    ash_cont = models.FloatField(verbose_name="خاکستر",unique=False, blank=True, null=True)
    therm_val = models.FloatField(verbose_name="ارزش حرارتی",unique=False, blank=True, null=True)
    fix_carbon = models.FloatField(verbose_name="کربن ثابت",unique=False, blank=True, null=True)
    moisture = models.FloatField(verbose_name="رطوبت",unique=False, blank=True, null=True)
    phosphor = models.FloatField(verbose_name="فسفر",unique=False, blank=True, null=True)
    plastometry = models.FloatField(verbose_name="پلاستومتری",unique=False, blank=True, null=True)
    reflectance = models.FloatField(verbose_name="قابلیت انعکاس نوری",unique=False, blank=True, null=True)
    sulphur = models.FloatField(verbose_name="گوگرد",unique=False, blank=True, null=True)
    vitrinite = models.FloatField(verbose_name="ویترینیت",unique=False, blank=True, null=True)
    volait_Mat = models.FloatField(verbose_name="مواد فرار",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.coal_lim
    class Meta:
        verbose_name = "ترانشه معدنی زغال"
        verbose_name_plural = "ترانشه معدنی زغال"       
        
class Co_Min_Trn_Pt(LinkedToLayerTable):
    coal_lim = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    trench_no = models.CharField(verbose_name="نام یا شماره ترانشه",max_length=100, unique=False, blank=True, null=True)
    type_trn = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد (آزیموت)",unique=False, blank=True, null=True)
    ash_cont = models.FloatField(verbose_name="خاکستر",unique=False, blank=True, null=True)
    therm_val = models.FloatField(verbose_name="ارزش حرارتی",unique=False, blank=True, null=True)
    fix_carbon = models.FloatField(verbose_name="کربن ثابت",unique=False, blank=True, null=True)
    moisture = models.FloatField(verbose_name="رطوبت",unique=False, blank=True, null=True)
    phosphor = models.FloatField(verbose_name="فسفر",unique=False, blank=True, null=True)
    plastometry = models.FloatField(verbose_name="پلاستومتری",unique=False, blank=True, null=True)
    reflectance = models.FloatField(verbose_name="قابلیت انعکاس نوری",unique=False, blank=True, null=True)
    sulphur = models.FloatField(verbose_name="گوگرد",unique=False, blank=True, null=True)
    vitrinite = models.FloatField(verbose_name="ویترینیت",unique=False, blank=True, null=True)
    volait_Mat = models.FloatField(verbose_name="مواد فرار",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.coal_lim
    class Meta:
        verbose_name = "ترانشه معدنی زغال"
        verbose_name_plural = "ترانشه معدنی زغال"              
        
class Co_Min_Trn_Pl(LinkedToLayerTable):
    coal_lim = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    trench_no = models.CharField(verbose_name="نام یا شماره ترانشه",max_length=100, unique=False, blank=True, null=True)
    type_trn = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد (آزیموت)",unique=False, blank=True, null=True)
    ash_cont = models.FloatField(verbose_name="خاکستر",unique=False, blank=True, null=True)
    therm_val = models.FloatField(verbose_name="ارزش حرارتی",unique=False, blank=True, null=True)
    fix_carbon = models.FloatField(verbose_name="کربن ثابت",unique=False, blank=True, null=True)
    moisture = models.FloatField(verbose_name="رطوبت",unique=False, blank=True, null=True)
    phosphor = models.FloatField(verbose_name="فسفر",unique=False, blank=True, null=True)
    plastometry = models.FloatField(verbose_name="پلاستومتری",unique=False, blank=True, null=True)
    reflectance = models.FloatField(verbose_name="قابلیت انعکاس نوری",unique=False, blank=True, null=True)
    sulphur = models.FloatField(verbose_name="گوگرد",unique=False, blank=True, null=True)
    vitrinite = models.FloatField(verbose_name="ویترینیت",unique=False, blank=True, null=True)
    volait_Mat = models.FloatField(verbose_name="مواد فرار",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.coal_lim
    class Meta:
        verbose_name = "ترانشه معدنی زغال"
        verbose_name_plural = "ترانشه معدنی زغال" 
        
class Co_Test_Pit_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    type_pit = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    ash_cont = models.FloatField(verbose_name="خاکستر",unique=False, blank=True, null=True)
    calorific = models.FloatField(verbose_name="ارزش حرارتی",unique=False, blank=True, null=True)  
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    aluminum = models.FloatField(verbose_name="عیار متوسط آلمینیوم",unique=False, blank=True, null=True)
    antimony = models.FloatField(verbose_name="عیار متوسط آنتیموان",unique=False, blank=True, null=True)
    arsenic = models.FloatField(verbose_name="عیار متوسط آرسنیک",unique=False, blank=True, null=True)
    barium = models.FloatField(verbose_name="عیار متوسط باریم",unique=False, blank=True, null=True)
    berylium = models.FloatField(verbose_name="عیار متوسط برلیوم",unique=False, blank=True, null=True)
    boron = models.FloatField(verbose_name="عیار متوسط بر",unique=False, blank=True, null=True)
    bromine = models.FloatField(verbose_name="عیار متوسط  برم",unique=False, blank=True, null=True)
    cadmium = models.FloatField(verbose_name="عیار متوسط کادمیوم",unique=False, blank=True, null=True)
    calcium = models.FloatField(verbose_name="عیار متوسط کلسیم",unique=False, blank=True, null=True)
    carbon = models.FloatField(verbose_name="عیار متوسط کربن",unique=False, blank=True, null=True)
    cesium = models.FloatField(verbose_name="عیار متوسط سزیم",unique=False, blank=True, null=True)
    chlorine = models.FloatField(verbose_name="عیار متوسط کلر",unique=False, blank=True, null=True)
    chromium = models.FloatField(verbose_name="عیار متوسط کروم",unique=False, blank=True, null=True)
    cobalt = models.FloatField(verbose_name="عیارمتوسط کبالت",unique=False, blank=True, null=True)
    copper = models.FloatField(verbose_name="عیارمتوسط مس",unique=False, blank=True, null=True)
    fix_carbon = models.FloatField(verbose_name="کربن ثابت",unique=False, blank=True, null=True)
    gallium = models.FloatField(verbose_name="عیارمتوسط گالیوم",unique=False, blank=True, null=True)
    gold = models.FloatField(verbose_name="عیارمتوسط طلا",unique=False, blank=True, null=True)
    hafnium = models.FloatField(verbose_name="عیارمتوسط هافنیوم",unique=False, blank=True, null=True)
    indium = models.FloatField(verbose_name="عیارمتوسط ایندیم",unique=False, blank=True, null=True)
    iridium = models.FloatField(verbose_name="عیارمتوسط ایریدیوم",unique=False, blank=True, null=True)
    iron = models.FloatField(verbose_name="عیارمتوسط آهن",unique=False, blank=True, null=True)
    lantanum = models.FloatField(verbose_name="عیارمتوسط لانتانیوم",unique=False, blank=True, null=True)
    lead = models.FloatField(verbose_name="عیارمتوسط سرب",unique=False, blank=True, null=True)
    lithium = models.FloatField(verbose_name="عیارمتوسط لیتیوم",unique=False, blank=True, null=True) 
    magnesium = models.FloatField(verbose_name="عیارمتوسط منیزیم",unique=False, blank=True, null=True)
    mangenese = models.FloatField(verbose_name="عیارمتوسط منگنز",unique=False, blank=True, null=True)
    mercury = models.FloatField(verbose_name="عیارمتوسط جیوه",unique=False, blank=True, null=True)
    moisture = models.FloatField(verbose_name="رطوبت",unique=False, blank=True, null=True)
    phosphor = models.FloatField(verbose_name="فسفر",unique=False, blank=True, null=True)
    reflectance = models.FloatField(verbose_name="بارتابش",unique=False, blank=True, null=True)
    sulphur = models.FloatField(verbose_name="گوگرد",unique=False, blank=True, null=True)
    sulfur = models.FloatField(verbose_name="عیارمتوسط گوگرد",unique=False, blank=True, null=True)
    strontium = models.FloatField(verbose_name="عیارمتوسط استرانسیم",unique=False, blank=True, null=True)
    sodium = models.FloatField(verbose_name="عیارمتوسط سدیم",unique=False, blank=True, null=True)
    silver = models.FloatField(verbose_name="عیارمتوسط نقره",unique=False, blank=True, null=True)
    selenium = models.FloatField(verbose_name="عیارمتوسط سلنیوم",unique=False, blank=True, null=True)
    tungsten = models.FloatField(verbose_name="عیارمتوسط تنگستن",unique=False, blank=True, null=True)
    titanuim = models.FloatField(verbose_name="عیارمتوسط تیتانیم",unique=False, blank=True, null=True)
    tin = models.FloatField(verbose_name="عیارمتوسط  قلع",unique=False, blank=True, null=True)
    thorium = models.FloatField(verbose_name="عیارمتوسط توریم",unique=False, blank=True, null=True)
    tellurium = models.FloatField(verbose_name="عیارمتوسط تلوریم",unique=False, blank=True, null=True)
    tantalium = models.FloatField(verbose_name="عیارمتوسط تانتالیم",unique=False, blank=True, null=True)
    uranium = models.FloatField(verbose_name="عیارمتوسط اورانیوم",unique=False, blank=True, null=True)
    vanadium = models.FloatField(verbose_name="عیارمتوسط وانادیوم",unique=False, blank=True, null=True)
    vitrinite = models.FloatField(verbose_name="قابلیت انعکاس نوری ویترینیت",unique=False, blank=True, null=True)
    volaitile_matter = models.FloatField(verbose_name="مواد فرار",unique=False, blank=True, null=True)
    ytterium = models.FloatField(verbose_name="عیارمتوسط ایتریم",unique=False, blank=True, null=True)
    ytterbium = models.FloatField(verbose_name="عیارمتوسط ایتربیم",unique=False, blank=True, null=True)    
    zirconium = models.FloatField(verbose_name="عیارمتوسط زیرکونیوم",unique=False, blank=True, null=True)
    zinc = models.FloatField(verbose_name="عیارمتوسط روی",unique=False, blank=True, null=True)   
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "چاهک زغال"
        verbose_name_plural = "چاهک زغال"               
        
class Iso_RF_T_Pl(LinkedToLayerTable):    
    depth_ele = models.FloatField(verbose_name="عدد عمقی",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.depth_ele
    class Meta:
        verbose_name = "خطوط هم ضخامت کف یا سقف"
        verbose_name_plural = "خطوط هم ضخامت کف یا سقف"   
        
        
class Key_bed_Pg(LinkedToLayerTable):
    abbrev = models.CharField(verbose_name="علامت اختصاری",max_length=100, unique=False, blank=True, null=True)
    fossil= models.CharField(verbose_name="فسیل",max_length=250, unique=False, blank=True, null=True)
    kb_thick = models.FloatField(verbose_name="ضخامت",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.abbrev 
    class Meta:
        verbose_name = "لایه راهنما"
        verbose_name_plural = "لایه راهنما"            
        
class Coal_Smpl_Lc_Pt(LinkedToLayerTable):
    sample_id = models.CharField(verbose_name="شماره نمونه",max_length=100, unique=False, blank=True, null=True)
    ash_cont = models.FloatField(verbose_name="خاکستر",unique=False, blank=True, null=True)
    therm_val = models.FloatField(verbose_name="ارزش حرارتی",unique=False, blank=True, null=True)
    fix_carbon = models.FloatField(verbose_name="کربن ثابت",unique=False, blank=True, null=True)
    moisture = models.FloatField(verbose_name="رطوبت",unique=False, blank=True, null=True)
    phosphor = models.FloatField(verbose_name="فسفر",unique=False, blank=True, null=True)
    plastometry = models.FloatField(verbose_name="پلاستومتری",unique=False, blank=True, null=True)
    reflectance = models.FloatField(verbose_name="قابلیت انعکاس نوری",unique=False, blank=True, null=True)
    sulphur = models.FloatField(verbose_name="گوگرد",unique=False, blank=True, null=True)
    vitrinite = models.FloatField(verbose_name="ویترینیت",unique=False, blank=True, null=True)
    volait_Mat = models.FloatField(verbose_name="مواد فرار",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.sample_id
    class Meta:
        verbose_name = "محل نمونه برداری زغال"
        verbose_name_plural = "محل نمونه برداری زغال"            

class Nes_Boundry_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مرز نامشخص"
        verbose_name_plural = "مرز نامشخص" 
        
class Oklon_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    strick = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    x = models.FloatField(verbose_name="مختصات x",unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="مختصات y",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "اکلون"
        verbose_name_plural = "اکلون"                
              
class Hole_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    wt_ty = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    x = models.FloatField(verbose_name="utm  در سیستم x مختصات ",unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="utm  در سیستم y مختصات ",unique=False, blank=True, null=True)
    z = models.FloatField(verbose_name="utm  در سیستم z مختصات ",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "چال"
        verbose_name_plural = "چال"                        
                
class Oxcide_Z_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زون اکسید"
        verbose_name_plural = "زون اکسید"    
                
class Tecto_Z_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    type_fault = models.CharField(verbose_name="نوع گسل",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زون تکتونیزه"
        verbose_name_plural = "زون تکتونیزه"

class Pillar_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=250, unique=False, blank=True, null=True)
    catagory = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="ازیموت",unique=False, blank=True, null=True)
    size = models.FloatField(verbose_name="اندازه",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = "پیلار"
        verbose_name_plural = "پیلار" 