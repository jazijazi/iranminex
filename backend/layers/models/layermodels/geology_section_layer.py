from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable

class Alteration_S_Pg(LinkedToLayerTable):
    alt_type = models.CharField(verbose_name= "نوع دگرساني سنگ", max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name= "نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    comment_fa = models.CharField(verbose_name= "توضیحات فارسی",max_length=250, unique=False, blank=True, null=True)
    comment_en = models.CharField(verbose_name= "توضیحات لاتین",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.alt_type 
    class Meta:
        verbose_name = "محدوده دگرسان شده در مقطع"
        verbose_name_plural = "محدوده دگرسان شده در مقطع"   
 
class BHole_LS_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره گمانه",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    drill_ty = models.CharField(verbose_name="نوع حفاری",max_length=100, unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="آزیموت گمانه",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق گمانه",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب گمانه",unique=False, blank=True, null=True)
    hole_ele = models.FloatField(verbose_name="ارتفاع محل دهانه گمانه",unique=False, blank=True, null=True)
    easting = models.FloatField(verbose_name="مختصات X گمانه بر روی محور",unique=False, blank=True, null=True)
    northing = models.FloatField(verbose_name="مختصاتY گمانه بر روی محور",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات ",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دهانه گمانه در مقطع"
        verbose_name_plural = "دهانه گمانه در مقطع"   
        
class BHole_PS_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره گمانه",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    drill_ty = models.CharField(verbose_name="نوع حفاری",max_length=100, unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="آزیموت گمانه",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق گمانه",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب گمانه",unique=False, blank=True, null=True)
    hole_ele = models.FloatField(verbose_name="ارتفاع محل دهانه گمانه",unique=False, blank=True, null=True)

    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تصوير گمانه در مقطع"
        verbose_name_plural = "تصوير گمانه در مقطع" 

class Coal_La_S_Pl(LinkedToLayerTable):
    abbrev = models.CharField(verbose_name="علامت اختصاری",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    lav_thicknes = models.FloatField(verbose_name="ضخامت متوسط لايه",unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.abbrev
    class Meta:
        verbose_name = "لایه زغال در مقطع"
        verbose_name_plural = "لایه زغال در مقطع"            
        
class Coal_La_S_Pg(LinkedToLayerTable):
    abbrev = models.CharField(verbose_name="علامت اختصاری",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    lav_thicknes = models.FloatField(verbose_name="ضخامت متوسط لايه",unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.abbrev
    class Meta:
        verbose_name = "لایه زغال در مقطع"
        verbose_name_plural = "لایه زغال در مقطع"  
       
class Dike_L_S_Pl(LinkedToLayerTable):
    dike_l_s = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    structure = models.CharField(verbose_name="نوع ساخت",max_length=100, unique=False, blank=True, null=True)
    texture = models.CharField(verbose_name="نوع بافت",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.dike_l_s
    class Meta:
        verbose_name = "دایک در مقطع"
        verbose_name_plural = "دایک در مقطع"  

class Ex_Tn_Prj_S_Pg(LinkedToLayerTable):
    ex_tn_prj = models.CharField(verbose_name="نام یا شناسه تونل اکتشافی",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.ex_tn_prj
    class Meta:
        verbose_name = "تصوير تونل اكتشافي در مقطع"
        verbose_name_plural = "تصوير تونل اكتشافي در مقطع"  

class Ex_Tn_Prj_S_Pl(LinkedToLayerTable):
    ex_tn_prj = models.CharField(verbose_name="نام یا شناسه تونل اکتشافی",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.ex_tn_prj
    class Meta:
        verbose_name = "تصوير تونل اكتشافي در مقطع"
        verbose_name_plural = "تصوير تونل اكتشافي در مقطع"          

class Fault_S_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام گسل",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    type_fault = models.CharField(verbose_name="نوع گسل",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد-آزیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "گسل در مقطع"
        verbose_name_plural = "گسل در مقطع"        

class Glg_Sec_P_Pl(LinkedToLayerTable):   
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)    
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.glg_sec_id
    class Meta:
        verbose_name = "پروفيل مقطع زمين شناسي"
        verbose_name_plural = "پروفيل مقطع زمين شناسي"     
 
class Oklon_LS_Pt(LinkedToLayerTable):
    oklon_id = models.CharField(verbose_name="شناسه اوکلون اكتشافي",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    northing = models.FloatField(verbose_name="مختصاتy چال بر روي محور",unique=False, blank=True, null=True)
    easting = models.FloatField(verbose_name="مختصات‌x چال بر روي محور",unique=False, blank=True, null=True)
    oklon_ele = models.FloatField(verbose_name="ارتفاع دهانه اوکلون اكتشافي",unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="آزيموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضيحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.oklon_id
    class Meta:
        verbose_name = "دهانه اوکلون در مقطع"
        verbose_name_plural = "دهانه اوکلون در مقطع"  

class Rck_Typ_Glg_S_Pg(LinkedToLayerTable):
    geo_unit = models.CharField(verbose_name= "نام لایه به اختصار", max_length=100, unique=False, blank=True, null=True)
    lable = models.CharField(verbose_name= "کد واحد سنگی", max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name= "نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    formation = models.CharField(verbose_name= "سازند",max_length=100, unique=False, blank=True, null=True)
    era = models.CharField(verbose_name= "دوران",max_length=100, unique=False, blank=True, null=True)
    period = models.CharField(verbose_name= "دوره",max_length=100, unique=False, blank=True, null=True)
    origin = models.CharField(verbose_name= "خاستگاه",max_length=100, unique=False, blank=True, null=True)
    structure = models.CharField(verbose_name="نوع ساخت",max_length=100, unique=False, blank=True, null=True)
    format_bo = models.CharField(verbose_name="نوع توده",max_length=100, unique=False, blank=True, null=True)
    complx = models.CharField(verbose_name="نام کمپلکس",max_length=100, unique=False, blank=True, null=True)
    series = models.CharField(verbose_name="نام سری",max_length=100, unique=False, blank=True, null=True)
    texture = models.CharField(verbose_name="نوع بافت",max_length=100, unique=False, blank=True, null=True)

    rock_mod = models.CharField(verbose_name= "مشخصات ظاهری",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.geo_unit
    class Meta:
        verbose_name = "تیپ سنگ شناسی  در مقطع"
        verbose_name_plural = "تیپ سنگ شناسی  در مقطع"  

class Test_Pit_LS_Pt(LinkedToLayerTable):
    pit_id = models.CharField(verbose_name="شناسه چاهک اكتشافي",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    type_t = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضيحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.pit_id
    class Meta:
        verbose_name = "دهانه چاهک در مقطع"
        verbose_name_plural = "دهانه چاهک در مقطع"  
        
class Unit_Bound_S_Pl(LinkedToLayerTable):   
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    contact = models.CharField(verbose_name="وضعیت همبری",max_length=100, unique=False, blank=True, null=True)
    contact_ty = models.CharField(verbose_name="نوع همبری",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)    
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "همبری واحدها  در مقطع"
        verbose_name_plural = "همبری واحدها  در مقطع"             
        
class Vein_S_Pg(LinkedToLayerTable):   
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    mnrl_cond = models.CharField(verbose_name="وضعیت کانی‌سازی",max_length=100, unique=False, blank=True, null=True)
    vein_condition = models.CharField(verbose_name="وضعیت رگه",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد-آزیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    m_thicknes = models.FloatField(verbose_name="ضخامت متوسط",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)    
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "رگه در مقطع"
        verbose_name_plural = "رگه در مقطع"           
        
class Vein_L_S_Pl(LinkedToLayerTable):   
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    mnrl_cond = models.CharField(verbose_name="وضعیت کانی‌سازی",max_length=100, unique=False, blank=True, null=True)
    vein_condition = models.CharField(verbose_name="وضعیت رگه",max_length=100, unique=False, blank=True, null=True)
    strike = models.FloatField(verbose_name="امتداد-آزیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dip_direction = models.FloatField(verbose_name="جهت شیب",unique=False, blank=True, null=True)
    m_thicknes = models.FloatField(verbose_name="ضخامت متوسط",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)    
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = " رگه در مقطع"
        verbose_name_plural = " رگه در مقطع"

class Struct_Zone_S_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)    
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زون ساختاری در مقطع"
        verbose_name_plural = "زون ساختاری در مقطع"  

class Struct_Zone_S_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    glg_sec_id = models.CharField(verbose_name="نام مقطع زمین شناسی",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)    
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زون ساختاری در مقطع"
        verbose_name_plural = "زون ساختاری در مقطع"  