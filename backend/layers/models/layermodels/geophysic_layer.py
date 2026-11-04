from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable

class Gph_Ano_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    priority = models.CharField(verbose_name="اولویت",max_length=100, unique=False, blank=True, null=True)
    det_method = models.CharField(verbose_name="روش تعیین",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده اميد بخش ژئوفيزيک"
        verbose_name_plural = "محدوده اميد بخش ژئوفيزيک"  

class A_Gph_Sec_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="آزیموت",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مقطع  ژئوفيزيک هوابرد"
        verbose_name_plural = "مقطع  ژئوفيزيک هوابرد"  

class A_Radiometric_Domains_Pg(LinkedToLayerTable):
    age = models.CharField(verbose_name="سن",max_length=100, unique=False, blank=True, null=True)
    lithology = models.CharField(verbose_name="جنس سنگ",max_length=100, unique=False, blank=True, null=True)
    origin = models.CharField(verbose_name="منشا",max_length=100, unique=False, blank=True, null=True)
    k = models.FloatField(verbose_name="پتاسیم",unique=False, blank=True, null=True)
    th = models.FloatField(verbose_name="توریوم",unique=False, blank=True, null=True)
    u = models.FloatField(verbose_name="اورانیوم",unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.age
    class Meta:
        verbose_name = "حوضه هاي راديومتري هوايي"
        verbose_name_plural = "حوضه هاي راديومتري هوايي"  
        
class Fault_Gph_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام سنجنده",max_length=100, unique=False, blank=True, null=True)
    type_fault = models.CharField(verbose_name="نوع گسل",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "گسل استنباط شده از ژئوفيزيک"
        verbose_name_plural = "گسل استنباط شده از ژئوفيزيک"  

class Gph_Lim_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    mthod = models.CharField(verbose_name="روش",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده مطالعات ژئوفیزیکی"
        verbose_name_plural = "محدوده مطالعات ژئوفیزیکی"         
        
class Gph_Intrusives_Pg(LinkedToLayerTable):
    sus = models.CharField(verbose_name="خودپذیری",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.sus
    class Meta:
        verbose_name = "توده هاي نفوذي حاصل از استنباط"
        verbose_name_plural = "توده هاي نفوذي حاصل از استنباط" 

        
class Gph_Sec_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    profile_spacing = models.FloatField(verbose_name="فاصله پروفیل ها",unique=False, blank=True, null=True)
    profile_strike = models.FloatField(verbose_name="امتداد پروفیل",unique=False, blank=True, null=True)
    end_x_coor = models.FloatField(verbose_name="مختصات X انتها",unique=False, blank=True, null=True)
    end_y_coor = models.FloatField(verbose_name="مختصاتY انتها",unique=False, blank=True, null=True)
    start_x_coor = models.FloatField(verbose_name="مختصات Xابتدا",unique=False, blank=True, null=True)
    start_y_coor = models.FloatField(verbose_name="مختصاتY ابتدا",unique=False, blank=True, null=True)
    mthod = models.CharField(verbose_name="روش",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پروفیل برداشت ژئوفیزیک"
        verbose_name_plural = "پروفیل برداشت ژئوفیزیک"                
        
class Gph_P_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    mthod = models.CharField(verbose_name="روش",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نقاط برداشت ژئوفيزيک"
        verbose_name_plural = "نقاط برداشت ژئوفيزيک" 

class GPS_Base_Station_Pt(LinkedToLayerTable):
    x = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    z = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.x
    class Meta:
        verbose_name = "GPS  نقطه ايستگاه مبناي"
        verbose_name_plural = "GPS  نقطه ايستگاه مبناي"         
        
class Gr_Field_Pt(LinkedToLayerTable):
    lithology = models.CharField(verbose_name="جنس سنگ",max_length=250, unique=False, blank=True, null=True)
    k = models.FloatField(verbose_name="درصد پتاسیم",unique=False, blank=True, null=True)
    th_ppm = models.FloatField(verbose_name="میزان غلظت توریم",unique=False, blank=True, null=True)
    u_ppm = models.FloatField(verbose_name="میزان غلظت اورانیوم",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.lithology
    class Meta:
        verbose_name = "برداشت زميني راديومتري"
        verbose_name_plural = "برداشت زميني راديومتري"   

class Rck_Typ_Rad_Pg(LinkedToLayerTable):
    origin = models.CharField(verbose_name="خاستگاه",max_length=100, unique=False, blank=True, null=True)
    age = models.CharField(verbose_name="سن واحد",max_length=100, unique=False, blank=True, null=True)
    symbol = models.CharField(verbose_name="نشانه",max_length=100, unique=False, blank=True, null=True)
    lithology = models.CharField(verbose_name="سنگ شناسی",max_length=100, unique=False, blank=True, null=True)  
    max_u = models.FloatField(verbose_name="ماکزیمم اورانیوم",unique=False, blank=True, null=True)
    min_u = models.FloatField(verbose_name="مینیمم اورانیوم",unique=False, blank=True, null=True)
    avg_u = models.FloatField(verbose_name="میانگین اورانیوم",unique=False, blank=True, null=True)
    sdu_u = models.FloatField(verbose_name="انحراف معیار اورانیوم",unique=False, blank=True, null=True)
    max_th = models.FloatField(verbose_name="ماکزیمم توریوم",unique=False, blank=True, null=True)
    min_th = models.FloatField(verbose_name="مینیمم توریوم",unique=False, blank=True, null=True)
    avg_th = models.FloatField(verbose_name="میانگین توریوم",unique=False, blank=True, null=True)
    sdu_th = models.FloatField(verbose_name="انحراف معیار توریوم",unique=False, blank=True, null=True)
    max_k = models.FloatField(verbose_name="ماکزیمم پتاسیم",unique=False, blank=True, null=True)
    min_k = models.FloatField(verbose_name="مینیمم پتاسیم",unique=False, blank=True, null=True)
    avg_k = models.FloatField(verbose_name="میانگین پتاسیم",unique=False, blank=True, null=True)
    sdu_k = models.FloatField(verbose_name="انحراف معیار پتاسیم",unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.depth
    class Meta:
        verbose_name = "تفکيک واحدهاي زمين شناسي بر اساس راديومتري"
        verbose_name_plural = "تفکيک واحدهاي زمين شناسي بر اساس راديومتري"            
        
class Rck_Typ_Mag_Pg(LinkedToLayerTable):
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)  
    origin = models.CharField(verbose_name="خاستگاه",max_length=100, unique=False, blank=True, null=True)
    sus = models.FloatField(verbose_name="خودپذيري",unique=False, blank=True, null=True)
    lithology = models.CharField(verbose_name="سنگ شناسی",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.depth
    class Meta:
        verbose_name = "واحد زمين شناسي حاصل از مغناطيس سنجي"
        verbose_name_plural = "واحد زمين شناسي حاصل از مغناطيس سنجي"       

class Rad_Ano_Pg(LinkedToLayerTable):
    type_m = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    minn = models.FloatField(verbose_name="حداقل",unique=False, blank=True, null=True)  
    maxx = models.FloatField(verbose_name="حداکثر",unique=False, blank=True, null=True)
    ave = models.FloatField(verbose_name="میانگین",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ناهنجاري راديومتري"
        verbose_name_plural = "ناهنجاري راديومتري" 
        
class Shallow_Magnetic_Ano_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "بي هنجاري هاي کم ژرف مغناطيسي"
        verbose_name_plural = "بي هنجاري هاي کم ژرف مغناطيسي"

class Gph_Contr_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    method = models.CharField(verbose_name="روش",max_length=100, unique=False, blank=True, null=True)
    value = models.CharField(verbose_name="مقدار",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "منحنی میزان ژیوفیزیک"
        verbose_name_plural = "منحنی میزان ژیوفیزیک"

class L_Grv_Ano_Pg(LinkedToLayerTable):
    type_m = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    minn = models.FloatField(verbose_name="حداقل",unique=False, blank=True, null=True)  
    maxx = models.FloatField(verbose_name="حداکثر",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.type_m
    class Meta:
        verbose_name = "ناهنجاري گرانی سنجی"
        verbose_name_plural = "ناهنجاري گرانی سنجی"

class Ip_Ano_Pg(LinkedToLayerTable):
    type_m = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    minn = models.FloatField(verbose_name="حداقل",unique=False, blank=True, null=True)  
    maxx = models.FloatField(verbose_name="حداکثر",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.type_m
    class Meta:
        verbose_name = "زون ناهنجاری پولاریزاسیون القایی"
        verbose_name_plural = "زون ناهنجاری پولاریزاسیون القایی"

class Megnetic_Body_Pg(LinkedToLayerTable):
    type_m = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    minn = models.FloatField(verbose_name="حداقل",unique=False, blank=True, null=True)  
    maxx = models.FloatField(verbose_name="حداکثر",unique=False, blank=True, null=True)
    ave = models.FloatField(verbose_name="میانگین",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.type_m
    class Meta:
        verbose_name = "انومالی مغناطیسی"
        verbose_name_plural = "انومالی مغناطیسی"

class Pnt_Gel_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=250, unique=False, blank=True, null=True)
    gph_profile_id = models.CharField(verbose_name="شناسه پروفیل برداشت مطالعات ژیوفیزیک",max_length=250, unique=False, blank=True, null=True)
    app_resis = models.FloatField(verbose_name="میزان مقاومت ظاهری",unique=False, blank=True, null=True)
    chargblity = models.FloatField(verbose_name="میزان شدت شارژابیلیته",unique=False, blank=True, null=True)
    intensity = models.FloatField(verbose_name="میزان شدت جریان",unique=False, blank=True, null=True)
    met_factor = models.FloatField(verbose_name="میزان فاکتور",unique=False, blank=True, null=True)
    poten_dif = models.FloatField(verbose_name="میزان اختلاف پوتانسیل",unique=False, blank=True, null=True)
    self_poten = models.FloatField(verbose_name="میزان خودپتانسیل",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نقاط برداشت ژئوالکتریک"
        verbose_name_plural = "نقاط برداشت ژئوالکتریک" 


class Brit_Struc_Gph_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=250, unique=False, blank=True, null=True)
    gph_st_type = models.CharField(verbose_name="نوع مطالعات ژیوفیزیکی",max_length=250, unique=False, blank=True, null=True)
    geophysic_scale = models.CharField(verbose_name="مقیاس مطالعات ژیوفیزیکی",max_length=250, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ساختار شکنا حاصل از ژیوفیزیک"
        verbose_name_plural = "ساختار شکنا حاصل از ژیوفیزیک" 

class Euler_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=250, unique=False, blank=True, null=True)
    x = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    x_euler = models.FloatField(verbose_name="طول اویلر",unique=False, blank=True, null=True)
    y_euler = models.FloatField(verbose_name="عرض اویلر",unique=False, blank=True, null=True)
    x_offset = models.FloatField(verbose_name="دور افت طولی",unique=False, blank=True, null=True)
    y_offset = models.FloatField(verbose_name="دور افت عرضی",unique=False, blank=True, null=True)
    dxy = models.FloatField(verbose_name="تغییرات افقی",unique=False, blank=True, null=True)
    dz = models.FloatField(verbose_name="تغییرات عمقی",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)  
    wndsize = models.FloatField(verbose_name="اندازه پنجره",unique=False, blank=True, null=True)  
    bckgrnd = models.FloatField(verbose_name="مقدار زمینه",unique=False, blank=True, null=True)  
    mask = models.CharField(verbose_name="ماسک",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "روش اویلر"
        verbose_name_plural = "روش اویلر" 


class Tillt_Contr_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    value = models.FloatField(verbose_name="مقدار",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "منحنی میزان زاویه تیلت"
        verbose_name_plural = "منحنی میزان زاویه تیلت"

class Mag_Grid_Pnt_Pt(LinkedToLayerTable):
    pointid = models.CharField(verbose_name="شناسه نقطه",max_length=100, unique=False, blank=True, null=True)
    downward = models.FloatField(verbose_name="ادامه فروسو به پایین",unique=False, blank=True, null=True)
    upward =  models.FloatField(verbose_name="ادامه فروسو به بالا",unique=False, blank=True, null=True)
    total_magnatic_feild = models.FloatField(verbose_name="شدت میدان مغناطیسی کل",unique=False, blank=True, null=True)
    tmi = models.FloatField(verbose_name="شدت میدان مغناطیسی باقیمانده",unique=False, blank=True, null=True)
    tilt = models.FloatField(verbose_name="تیلت شدت میدان مغناطیسی باقیمانده",unique=False, blank=True, null=True)
    tmi_as = models.FloatField(verbose_name="سیگنال تحلیل شدت میدان مغناطیسی باقیمانده",unique=False, blank=True, null=True)
    tmi_vdi = models.FloatField(verbose_name="مشتق قایم  مرتبه اول شدت باقیمانده",unique=False, blank=True, null=True)
    tmi_hdi = models.FloatField(verbose_name="مشتق مرتبه اول شدت باقیمانده",unique=False, blank=True, null=True)
    rtp = models.FloatField(verbose_name="برگردان به قطب شدت میدان مغناطیسی",unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.pointid
    class Meta:
        verbose_name = "نقاط گریدهای مغناطیسی"
        verbose_name_plural = "نقاط گریدهای مغناطیسی"

class Pnt_Elmag_Pt(LinkedToLayerTable):
    pointid = models.CharField(verbose_name="شناسه نقطه",max_length=100, unique=False, blank=True, null=True)
    appa_conduct = models.FloatField(verbose_name="میزان رسانایی ظاهری",unique=False, blank=True, null=True)
    gph_profile_id = models.CharField(verbose_name="شناسه پروفیل برداشت مطالعات ژیوفیزیک",max_length=100,unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.pointid
    class Meta:
        verbose_name = "نقاط برداشت الکترومغناطیس"
        verbose_name_plural = "نقاط برداشت الکترومغناطیس"

class Pnt_Rad_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    gph_profile_id = models.CharField(verbose_name="شناسه پروفیل برداشت مطالعات ژیوفیزیک",max_length=100,unique=False, blank=True, null=True)
    app_resis = models.FloatField(verbose_name="میزان مقاومت ظاهری",unique=False, blank=True, null=True)
    u = models.FloatField(verbose_name="میزان اورانیوم",unique=False, blank=True, null=True)
    th = models.FloatField(verbose_name="میزان توریوم",unique=False, blank=True, null=True)
    k = models.FloatField(verbose_name="میزان پتاسیم",unique=False, blank=True, null=True)
    tc = models.FloatField(verbose_name="شمارش کل",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نقاط برداشت رادیومتریک"
        verbose_name_plural = "نقاط برداشت رادیومتریک"

class Pnt_Grv_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    gph_profile_id = models.CharField(verbose_name="شناسه پروفیل برداشت مطالعات ژیوفیزیک",max_length=100,unique=False, blank=True, null=True)
    boug_ano = models.FloatField(verbose_name="میزان آنومالی بوگه",unique=False, blank=True, null=True)
    grv_rsd = models.FloatField(verbose_name="میزان آنومالی باقی مانده گرانی",unique=False, blank=True, null=True)
    z = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نقاط برداشت گرانی"
        verbose_name_plural = "نقاط برداشت گرانی"

class Pnt_Gmag_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    gph_profile_id = models.CharField(verbose_name="شناسه پروفیل برداشت مطالعات ژیوفیزیک",max_length=100,unique=False, blank=True, null=True)
    precision = models.CharField(verbose_name="دقت",max_length=100, unique=False, blank=True, null=True)
    tfi = models.FloatField(verbose_name="میزان شدت کل میدان مغناطیسی",unique=False, blank=True, null=True)
    igrf = models.FloatField(verbose_name="حد زمینه شدت میدان مغناطیسی",unique=False, blank=True, null=True)
    declination = models.FloatField(verbose_name="شیب شدت میدان مغناطیسی",unique=False, blank=True, null=True)
    dur_cor = models.FloatField(verbose_name="تصحیح روزانه",unique=False, blank=True, null=True)
    inclination = models.FloatField(verbose_name="زاویه میل",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نقاط برداشت مغناطیس"
        verbose_name_plural = "نقاط برداشت مغناطیس"

class Magnetic_Linear_Trend_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "روندهای خطی ناهنجاری مغناطیسی"
        verbose_name_plural = "روندهای خطی ناهنجاری مغناطیسی"
