from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable


class B_Model_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره بلوک",max_length=100, unique=False, blank=True, null=True)
    class_B = models.CharField(verbose_name="کلاس",max_length=100, unique=False, blank=True, null=True)
    elemnt_ty = models.CharField(verbose_name="نوع عنصر",max_length=100, unique=False, blank=True, null=True)
    data_ty = models.CharField(verbose_name="نوع داده",max_length=100, unique=False, blank=True, null=True)
    method = models.CharField(verbose_name="روش تعیین",max_length=100, unique=False, blank=True, null=True)
    lower_lim = models.FloatField(verbose_name="حد پایین آنومالی",unique=False, blank=True, null=True)
    upper_lim = models.FloatField(verbose_name="حد بالا آنومالی",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مدل بلوکی"
        verbose_name_plural = "مدل بلوکی"

class B_Model_Zone_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره بلوک",max_length=100, unique=False, blank=True, null=True)
    class_B = models.CharField(verbose_name="کلاس",max_length=100, unique=False, blank=True, null=True)
    x = models.FloatField(verbose_name="طول", unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="عرض", unique=False, blank=True, null=True)
    z = models.FloatField(verbose_name="ارتفاع", unique=False, blank=True, null=True)
    sub_x = models.FloatField(verbose_name="sub_x", unique=False, blank=True, null=True)
    sub_y = models.FloatField(verbose_name="sub_y", unique=False, blank=True, null=True)
    sub_z = models.FloatField(verbose_name="sub_z", unique=False, blank=True, null=True)
    n = models.FloatField(verbose_name="تعداد", unique=False, blank=True, null=True)
    avg_dist = models.FloatField(verbose_name="میانگین فاصله", unique=False, blank=True, null=True)
    min_dist = models.FloatField(verbose_name="حداقل فاصله", unique=False, blank=True, null=True)
    density = models.FloatField(verbose_name="وزن مخصوص", unique=False, blank=True, null=True)
    ore_tonnag = models.FloatField(verbose_name="تناژ ماده معدنی", unique=False, blank=True, null=True)
    el_tonnag = models.FloatField(verbose_name="تناژ عنصر", unique=False, blank=True, null=True)
    variance = models.FloatField(verbose_name="واریانس", unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زون بندی مدل بلوکی"
        verbose_name_plural = "زون بندی مدل بلوکی"
        
class Tunnel_Pl(LinkedToLayerTable):    
    type_Tu = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = "تونل اکتشافی"
        verbose_name_plural = "تونل اکتشافی"                          

class Vein_Pg_Trn_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    trench_id = models.CharField(verbose_name="شناسه ترانشه",max_length=100, unique=False, blank=True, null=True)
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
        verbose_name = "رگه در ترانشه"
        verbose_name_plural = "رگه در ترانشه"

class Vein_L_Trn_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    trench_id = models.CharField(verbose_name="شناسه ترانشه",max_length=100, unique=False, blank=True, null=True)
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
        verbose_name = "رگه در ترانشه"
        verbose_name_plural = "رگه در ترانشه"

class Vein_Pg_Tu_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    tunnel_id = models.CharField(verbose_name="شناسه تونل",max_length=100, unique=False, blank=True, null=True)
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
        verbose_name = "رگه در تونل"
        verbose_name_plural = "رگه در تونل"

class Vein_L_Tu_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    tunnel_id = models.CharField(verbose_name="شناسه تونل",max_length=100, unique=False, blank=True, null=True)
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
        verbose_name = "رگه در تونل"
        verbose_name_plural = "رگه در تونل"  

class Fault_Tu_Pl(LinkedToLayerTable):
    fault_tu = models.CharField(verbose_name="نام گسل",max_length=100, unique=False, blank=True, null=True)
    tunnel_id = models.CharField(verbose_name="شناسه تونل",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.fault_tu
    class Meta:
        verbose_name = "گسل تونل"
        verbose_name_plural = "گسل تونل"          
        
class Fault_Trn_Pl(LinkedToLayerTable):
    fault_trn = models.CharField(verbose_name="نام گسل",max_length=100, unique=False, blank=True, null=True)
    trench_id = models.CharField(verbose_name="شناسه ترانشه",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.fault_trn
    class Meta:
        verbose_name = " گسل ترانشه"
        verbose_name_plural = "گسل ترانشه"    
        
class Exp_Shaft_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="شماره شفت",max_length=100, unique=False, blank=True, null=True)
    dep_name = models.CharField(verbose_name="نام کانسار",max_length=100, unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="آزیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    hole_ele = models.FloatField(verbose_name="ارتفاع دهانه شفت اکتشافی",unique=False, blank=True, null=True)
    easting = models.FloatField(verbose_name="دهانه شفت اکتشافی X مختصات",unique=False, blank=True, null=True)
    northing = models.FloatField(verbose_name="دهانه شفت اکتشافی Y مختصات",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شفت اکتشافی"
        verbose_name_plural = "شفت اکتشافی"   

class Exp_Shaft_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="شماره شفت",max_length=100, unique=False, blank=True, null=True)
    dep_name = models.CharField(verbose_name="نام کانسار",max_length=100, unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="آزیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    hole_ele = models.FloatField(verbose_name="ارتفاع دهانه شفت اکتشافی",unique=False, blank=True, null=True)
    easting = models.FloatField(verbose_name="دهانه شفت اکتشافی X مختصات",unique=False, blank=True, null=True)
    northing = models.FloatField(verbose_name="دهانه شفت اکتشافی Y مختصات",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شفت اکتشافی"
        verbose_name_plural = "شفت اکتشافی"    

class Alteratn_Tu_Pg(LinkedToLayerTable):
    tunnel_id = models.CharField(verbose_name="شناسه تونل",max_length=100, unique=False, blank=True, null=True)
    alt_tu = models.CharField(verbose_name="نوع دگرسانی",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.tunnel_id
    class Meta:
        verbose_name = "محدوده دگرسان تونل"
        verbose_name_plural = "محدوده دگرسان تونل"       

class Alteratn_Trn_Pg(LinkedToLayerTable):
    trench_id = models.CharField(verbose_name="شناسه ترانشه",max_length=100, unique=False, blank=True, null=True)
    alt_trn = models.CharField(verbose_name="نوع دگرسانی",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.trench_id
    class Meta:
        verbose_name = "محدوده دگرسان ترانشه"
        verbose_name_plural = "محدوده دگرسان ترانشه"            

class Rck_Typ_Tu_Pg(LinkedToLayerTable):
    geo_unit = models.CharField(verbose_name="نام واحد سنگ شناسی",max_length=100, unique=False, blank=True, null=True)
    tunnel_id = models.CharField(verbose_name="شناسه تونل",max_length=100, unique=False, blank=True, null=True)
    intrusion_age = models.CharField(verbose_name="زمان نفوذ",max_length=100, unique=False, blank=True, null=True)
    assort = models.CharField(verbose_name="جور شدگی",max_length=100, unique=False, blank=True, null=True)
    bedding = models.CharField(verbose_name="لایه بندی",max_length=100, unique=False, blank=True, null=True)
    complex_tu = models.CharField(verbose_name="نام کمپلکس",max_length=100, unique=False, blank=True, null=True)
    format_bo = models.CharField(verbose_name="نوع توده",max_length=100, unique=False, blank=True, null=True)
    formation = models.CharField(verbose_name="نام سازند",max_length=100, unique=False, blank=True, null=True)
    rock_mod = models.CharField(verbose_name="مشخصه ظاهری",max_length=100, unique=False, blank=True, null=True)
    series = models.CharField(verbose_name="نام سری",max_length=100, unique=False, blank=True, null=True)
    structure = models.CharField(verbose_name="نوع ساخت",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.geo_unit
    class Meta:
        verbose_name = "تیپ سنگ شناسی تونل"
        verbose_name_plural = "تیپ سنگ شناسی تونل" 

class Rck_Typ_Trn_Pg(LinkedToLayerTable):
    geo_unit = models.CharField(verbose_name="نام واحد سنگ شناسی",max_length=100, unique=False, blank=True, null=True)
    trench_id = models.CharField(verbose_name="شناسه ترانشه",max_length=100, unique=False, blank=True, null=True)
    intrusion_age = models.CharField(verbose_name="زمان نفوذ",max_length=100, unique=False, blank=True, null=True)
    assort = models.CharField(verbose_name="جور شدگی",max_length=100, unique=False, blank=True, null=True)
    bedding = models.CharField(verbose_name="لایه بندی",max_length=100, unique=False, blank=True, null=True)
    complex_trn = models.CharField(verbose_name="نام کمپلکس",max_length=100, unique=False, blank=True, null=True)
    format_bo = models.CharField(verbose_name="نوع توده",max_length=100, unique=False, blank=True, null=True)
    formation = models.CharField(verbose_name="نام سازند",max_length=100, unique=False, blank=True, null=True)
    rock_mod = models.CharField(verbose_name="مشخصه ظاهری",max_length=100, unique=False, blank=True, null=True)
    series = models.CharField(verbose_name="نام سری",max_length=100, unique=False, blank=True, null=True)
    structure = models.CharField(verbose_name="نوع ساخت",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.geo_unit
    class Meta:
        verbose_name = "تیپ سنگ شناسی ترانشه"
        verbose_name_plural = "تیپ سنگ شناسی ترانشه"  
        
class Exp_Tnl_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام تونل",max_length=100, unique=False, blank=True, null=True)
    levelـ = models.FloatField(verbose_name="تراز",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    easting = models.FloatField(verbose_name="مختصات x داهنه ",unique=False, blank=True, null=True)
    northing = models.FloatField(verbose_name="مختصات y دهانه ",unique=False, blank=True, null=True)
    tu_ele = models.FloatField(verbose_name="ارتفاع سطح",unique=False, blank=True, null=True)
    hole_ele = models.FloatField(verbose_name="ارتفاع دهانه",unique=False, blank=True, null=True)
    azimuth  = models.FloatField(verbose_name="ازیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dep_n = models.CharField(verbose_name="نام کانسار",max_length=250, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تونل اکتشافی"
        verbose_name_plural = "تونل اکتشافی"      
        
class Exp_Tnl_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام تونل",max_length=100, unique=False, blank=True, null=True)
    levelـ = models.FloatField(verbose_name="تراز",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    easting = models.FloatField(verbose_name="مختصات x داهنه ",unique=False, blank=True, null=True)
    northing = models.FloatField(verbose_name="مختصات y دهانه ",unique=False, blank=True, null=True)
    tu_ele = models.FloatField(verbose_name="ارتفاع سطح",unique=False, blank=True, null=True)
    hole_ele = models.FloatField(verbose_name="ارتفاع دهانه",unique=False, blank=True, null=True)
    azimuth  = models.FloatField(verbose_name="ازیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dep_n = models.CharField(verbose_name="نام کانسار",max_length=250, unique=False, blank=True, null=True)

    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تونل اکتشافی"
        verbose_name_plural = "تونل اکتشافی"       
        
class Exp_Tnl_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام تونل",max_length=100, unique=False, blank=True, null=True)
    levelـ = models.FloatField(verbose_name="تراز",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    easting = models.FloatField(verbose_name="مختصات x داهنه ",unique=False, blank=True, null=True)
    northing = models.FloatField(verbose_name="مختصات y دهانه ",unique=False, blank=True, null=True)
    tu_ele = models.FloatField(verbose_name="ارتفاع سطح",unique=False, blank=True, null=True)
    hole_ele = models.FloatField(verbose_name="ارتفاع دهانه",unique=False, blank=True, null=True)
    azimuth  = models.FloatField(verbose_name="ازیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    dep_n = models.CharField(verbose_name="نام کانسار",max_length=250, unique=False, blank=True, null=True)

    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تونل اکتشافی"
        verbose_name_plural = "تونل اکتشافی"          
        

class Test_Pit_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    type_p = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع دهانه چاهک",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    x = models.FloatField(verbose_name="مختصات x",unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="مختصات y",unique=False, blank=True, null=True)
    date = models.DateField(verbose_name="تاریخ",auto_now=False,auto_now_add=False,null=True,blank=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "چاهک"
        verbose_name_plural = "چاهک"             

class BHole_P_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره گمانه",max_length=100, unique=False, blank=True, null=True)
    drill_ty = models.CharField(verbose_name="نوع حفاری پیشنهادی",max_length=100, unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="آزیموت گمانه",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق گمانه",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب گمانه",unique=False, blank=True, null=True)
    hole_ele = models.FloatField(verbose_name="ارتفاع محل دهانه گمانه",unique=False, blank=True, null=True)
    easting = models.FloatField(verbose_name="مختصات X گمانه بر روی محور",unique=False, blank=True, null=True)
    northing = models.FloatField(verbose_name="مختصاتY گمانه بر روی محور",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "گمانه پیشنهادی"
        verbose_name_plural = "گمانه پیشنهادی"             
        
class Exp_Smpl_Pt(LinkedToLayerTable):
    sample_id = models.CharField(verbose_name="شناسه نمونه",max_length=100, unique=False, blank=True, null=True)
    excavat_ty = models.CharField(verbose_name="نوع حفریات",max_length=100, unique=False, blank=True, null=True)
    
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
        return self.sample_id
    class Meta:
        verbose_name = "نمونه برداری اکتشافی"
        verbose_name_plural = "نمونه برداری اکتشافی"                     
        
        
class Collar_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="شماره گمانه",max_length=100, unique=False, blank=True, null=True)
    rig_name = models.CharField(verbose_name="نام دستگاه حفاری",max_length=100, unique=False, blank=True, null=True)
    lab_name = models.CharField(verbose_name="نام آزمایشگاه",max_length=100, unique=False, blank=True, null=True)
    drill_co = models.CharField(verbose_name="نام شرکت حفار",max_length=100, unique=False, blank=True, null=True)
    device = models.CharField(verbose_name="نام دستگاه انحراف سنج",max_length=100, unique=False, blank=True, null=True)
    drill_ty = models.CharField(verbose_name="نوع حفاری",max_length=100, unique=False, blank=True, null=True)
    northing = models.FloatField(verbose_name="دهانه گمانه Yمختصات",unique=False, blank=True, null=True)
    easting = models.FloatField(verbose_name="دهانه گمانه X مختصات",unique=False, blank=True, null=True)
    elevation = models.FloatField(verbose_name="ارتفاع محل دهانه گمانه",unique=False, blank=True, null=True)
    diameter = models.IntegerField(verbose_name="قطر حفاری",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق حفاری",unique=False, blank=True, null=True)
    start_date = models.DateField(verbose_name="تاریخ شروع حفاری",auto_now=False,auto_now_add=False,null=True,blank=True)
    end_date = models.DateField(verbose_name="تاریخ اتمام حفاری",auto_now=False,auto_now_add=False,null=True,blank=True)
    surv_date = models.DateField(verbose_name="تاریخ انحراف سنجی",auto_now=False,auto_now_add=False,null=True,blank=True)
    core_shed = models.CharField(verbose_name="محل انبار مغزه ها",max_length=100, unique=False, blank=True, null=True)
    water_t = models.CharField(verbose_name="عمق آب زیرزمینی",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دهانه گمانه"
        verbose_name_plural = "دهانه گمانه"   
        
class Trn_sec_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد (آزیموت)",unique=False, blank=True, null=True)
    st_x_coor = models.FloatField(verbose_name="ابتدا X مختصات",unique=False, blank=True, null=True)
    st_y_coor = models.FloatField(verbose_name="ابتدا Y مختصات",unique=False, blank=True, null=True)
    end_x_coor = models.FloatField(verbose_name="انتها X مختصات",unique=False, blank=True, null=True)
    end_x_coor = models.FloatField(verbose_name="انتها Y مختصات",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مقطع زمین شناسی ترانشه"
        verbose_name_plural = "مقطع زمین شناسی ترانشه"   

class F_C_Pnt_Trn_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    or_height = models.FloatField(verbose_name="ارتفاع ارتومتریک",unique=False, blank=True, null=True)
    x = models.FloatField(verbose_name="Xمختصات",unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="Yمختصات",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نقطه کنترل مسطحاتی و ارتفاعی در ترانشه"
        verbose_name_plural = "نقطه کنترل مسطحاتی و ارتفاعی در ترانشه" 
        
class Spot_H_Trn_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع ارتومتریک",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نقطه ارتفاعی در ترانشه"
        verbose_name_plural = "نقطه ارتفاعی در ترانشه" 


class Vertical_Section_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مقطع مدل بلوکی"
        verbose_name_plural = "مقطع مدل بلوکی"          

class Devil_Pt(LinkedToLayerTable):
    coal_lim = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    devil_no = models.CharField(verbose_name="شماره دویل",max_length=100, unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.coal_lim
    class Meta:
        verbose_name = "دویل"
        verbose_name_plural = "دویل"              
        
class Devil_Pl(LinkedToLayerTable):
    coal_lim = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    devil_no = models.CharField(verbose_name="شماره دویل",max_length=100, unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.coal_lim
    class Meta:
        verbose_name = "دویل"
        verbose_name_plural = "دویل"              

class Desandry_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    des_no = models.CharField(verbose_name="شماره دویل",max_length=100, unique=False, blank=True, null=True)
    azimute = models.FloatField(verbose_name="آزیموت",unique=False, blank=True, null=True)
    dip = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.coal_lim
    class Meta:
        verbose_name = "دساندری"
        verbose_name_plural = "دساندری"              

class Extraction_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام تونل",max_length=100, unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "بخش استخراج شده"
        verbose_name_plural = "بخش استخراج شده"     

class Well_Exp_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    typ_p = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    x = models.FloatField(verbose_name="Xمختصات",unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="Yمختصات",unique=False, blank=True, null=True)
    date = models.DateField(verbose_name="تاریخ",auto_now=False,auto_now_add=False,null=True,blank=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "چاه اکتشافی"
        verbose_name_plural = "چاه اکتشافی" 

class Exp_Opening_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    lvl = models.FloatField(verbose_name="تراز",unique=False, blank=True, null=True)
    # typ = models.FloatField(verbose_name="نوع",unique=False, blank=True, null=True)
    typ =  models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "بازکننده"
        verbose_name_plural = "بازکننده"

class Exp_Opening_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    lvl = models.FloatField(verbose_name="تراز",unique=False, blank=True, null=True)
    # typ = models.FloatField(verbose_name="نوع",unique=False, blank=True, null=True)
    typ =  models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "بازکننده"
        verbose_name_plural = "بازکننده"

class Face_Brick_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام ",max_length=250, unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="ضخامت",unique=False, blank=True, null=True)
    slope = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    grade = models.FloatField(verbose_name="عیار ماده معدنی",unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="میزان روباره",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = "سینه کار اکتشافی"
        verbose_name_plural = "سینه کار اکتشافی" 

class Face_Brick_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام ",max_length=250, unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="ضخامت",unique=False, blank=True, null=True)
    slope = models.FloatField(verbose_name="شیب",unique=False, blank=True, null=True)
    azimuth = models.FloatField(verbose_name="امتداد",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    grade = models.FloatField(verbose_name="عیار ماده معدنی",unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="میزان روباره",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 

    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = "سینه کار اکتشافی"
        verbose_name_plural = "سینه کار اکتشافی"