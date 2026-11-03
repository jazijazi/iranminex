from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable


class Wireless_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "وایرلس"
        verbose_name_plural = "وایرلس"

class Light_Bar_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    voltages = models.FloatField(verbose_name="ولتاژ",unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "چراغ روشنایی"
        verbose_name_plural = "چراغ روشنایی"

class Light_Bar_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    voltages = models.FloatField(verbose_name="ولتاژ",unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "چراغ روشنایی"
        verbose_name_plural = "چراغ روشنایی"

class Administrative_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "منطقه اداری"
        verbose_name_plural = "منطقه اداری"   

class Administrative_Area_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "منطقه اداری"
        verbose_name_plural = "منطقه اداری"


 
class Bench_Mark_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    x = models.FloatField(verbose_name="xمختصات",unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="yمختصات",unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    elevation = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ایستگاه نقشه برداری"
        verbose_name_plural = "ایستگاه نقشه برداری"            
 
class Bld_Blk_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    condition = models.CharField(verbose_name="وضعیت",max_length=100, unique=False, blank=True, null=True)
    build_ty = models.CharField(verbose_name="نوع ساختمان",max_length=100, unique=False, blank=True, null=True)
    ceiling_ty = models.CharField(verbose_name="نوع سقف",max_length=100, unique=False, blank=True, null=True)
    comment= models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "بلوک ساختمانی "
        verbose_name_plural = "بلوک ساختمانی "

class Bld_Blk_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    condition = models.CharField(verbose_name="وضعیت",max_length=100, unique=False, blank=True, null=True)
    build_ty = models.CharField(verbose_name="نوع ساختمان",max_length=100, unique=False, blank=True, null=True)
    ceiling_ty = models.CharField(verbose_name="نوع سقف",max_length=100, unique=False, blank=True, null=True)
    comment= models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "بلوک ساختمانی "
        verbose_name_plural = "بلوک ساختمانی " 

class Bridge_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پل"
        verbose_name_plural = "پل"    

class Bridge_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پل"
        verbose_name_plural = "پل"    

class Cam_Net_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)  
    type_cam = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment= models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = "شبکه دوربین"
        verbose_name_plural = "شبکه دوربین"  

class Camera_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل اسقرار",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دوربین"
        verbose_name_plural = "دوربین"  

class Camping_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محل استراحت"
        verbose_name_plural = "محل استراحت"          

class Cave_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "غار"
        verbose_name_plural = "غار"  
        
class Cemetery_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "قبرستان"
        verbose_name_plural = "قبرستان"

class Shrine_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "امام زاده"
        verbose_name_plural = "امام زاده"

class Shrine_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "امام زاده"
        verbose_name_plural = "امام زاده"

class Place_Worship_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = " مسجد"
        verbose_name_plural = " مسجد"

class Place_Worship_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = " مسجد"
        verbose_name_plural = " مسجد"
       
class Channel_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    mat_trans = models.CharField(verbose_name="نوع ماده حمل شونده",max_length=100, unique=False, blank=True, null=True)
    material = models.CharField(verbose_name="جنس مواد",max_length=100, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کانال"
        verbose_name_plural = "کانال"  
                
class City_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهر" 
        
class Com_Tow_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    mdl = models.CharField(verbose_name="",max_length=100, unique=False, blank=True, null=True)
    elevation = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دکل مخابراتی"
        verbose_name_plural = "دکل مخابراتی"         
        
class Contour_Pl(LinkedToLayerTable):    
    type_cnt = models.CharField(verbose_name="نوع منحنی",max_length=100, unique=False, blank=True, null=True)
    or_height = models.FloatField(verbose_name="ارتفاع ارتومتریک",unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = "منحنی میزان"
        verbose_name_plural = "منحنی میزان" 

class Cutting_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = "بریدگی"
        verbose_name_plural = "بریدگی"           

class Dam_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    capacity_vol = models.FloatField(verbose_name="ظرفیت حجمی",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    type_dam = models.CharField(verbose_name="نوع سد",max_length=100, unique=False, blank=True, null=True)
    material = models.CharField(verbose_name="جنس مواد",max_length=100, unique=False, blank=True, null=True)
    dam_usage = models.CharField(verbose_name="کاریری سد",max_length=100, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سد"
        verbose_name_plural = "سد"  
        
class Ditch_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "جدول"
        verbose_name_plural = "جدول"  

class Dispasal_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محل جمع آوری زباله"
        verbose_name_plural = "محل جمع آوری زباله"                 

class Dyke_T_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل اسقرار",max_length=100, unique=False, blank=True, null=True)
    status = models.CharField(verbose_name="وضعیت کاربردی",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آب بندان"
        verbose_name_plural = "آب بندان"    

class Dyke_T_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل اسقرار",max_length=100, unique=False, blank=True, null=True)
    status = models.CharField(verbose_name="وضعیت کاربردی",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آب بندان"
        verbose_name_plural = "آب بندان"                         
                
        
class Embankm_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "لبه خاکریز"
        verbose_name_plural = "لبه خاکریز"  
        
class Escarpment_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پرتگاه"
        verbose_name_plural = "پرتگاه"                 
                
class Escarpment_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پرتگاه"
        verbose_name_plural = "پرتگاه"          
 
class F_C_Pnt_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    or_height = models.FloatField(verbose_name="ارتفاع ارتومتریک",unique=False, blank=True, null=True)
    x = models.FloatField(verbose_name="xمختصات",unique=False, blank=True, null=True)
    y = models.FloatField(verbose_name="yمختصات",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نقطه کنترل مسطحاتی و ارتفاعی"
        verbose_name_plural = "نقطه کنترل مسطحاتی و ارتفاعی"  
        
class Factory_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام ",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کارخانه"
        verbose_name_plural = "کارخانه"

class Factory_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام ",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کارخانه"
        verbose_name_plural = "کارخانه"    

class Fence_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل اسقرار",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "حصار"
        verbose_name_plural = "حصار"      

class Flood_way_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مسیل"
        verbose_name_plural = "مسیل"            

class Industrial_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    activity = models.CharField(verbose_name="فعالیت غالب",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مراکز صنعتی"
        verbose_name_plural = "مراکز صنعتی" 
        

class Service_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    service_typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مراکز خدماتی"
        verbose_name_plural = "مراکز خدماتی" 

class Service_Area_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    service_typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مراکز خدماتی"
        verbose_name_plural = "مراکز خدماتی" 

class Industrial_Complex_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="مجتمع صنعتی",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مجتمع صنعتی"
        verbose_name_plural = "مجتمع صنعتی"        
                        
class Installation_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کارگاه"
        verbose_name_plural = "کارگاه"   
                
class Kiosk_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کیوسک"
        verbose_name_plural = "کیوسک"  

class Kiosk_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کیوسک"
        verbose_name_plural = "کیوسک"                
        
class Lake_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    specefic = models.CharField(verbose_name="مشخصات",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دریاچه"
        verbose_name_plural = "دریاچه"         

class Land_Cover_Pg(LinkedToLayerTable):
    covr_type = models.CharField(verbose_name="نوع کاربري و پوشش",max_length=100, unique=False, blank=True, null=True)
    ara = models.FloatField(verbose_name="مساحت",unique=False, blank=True, null=True)
    wat_sys_ty = models.CharField(verbose_name="نحوه آبیاری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.covr_type
    class Meta:
        verbose_name = "کاربری و پوشش"
        verbose_name_plural = "کاربری و پوشش"   

class Land_Cover_Pt(LinkedToLayerTable):
    covr_type = models.CharField(verbose_name="نوع کاربري و پوشش",max_length=100, unique=False, blank=True, null=True)
    ara = models.FloatField(verbose_name="مساحت",unique=False, blank=True, null=True)
    wat_sys_ty = models.CharField(verbose_name="نحوه آبیاری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.covr_type
    class Meta:
        verbose_name = "کاربری و پوشش"
        verbose_name_plural = "کاربری و پوشش"   

class Limit_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "حد"
        verbose_name_plural = "حد"  
        
class Medical_center_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت",unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مرکز درمانی"
        verbose_name_plural = "مرکز درمانی"

class Medical_center_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت",unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مرکز درمانی"
        verbose_name_plural = "مرکز درمانی"   
        
class Mine_Site_Area_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    mineral_ty = models.CharField(verbose_name="نوع ماده معدنی",max_length=100, unique=False, blank=True, null=True)
    mine_type = models.CharField(verbose_name="نوع معدن",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سایت معدن"
        verbose_name_plural = "سایت معدن" 
        
class Mine_Site_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    mineral_ty = models.CharField(verbose_name="نوع ماده معدنی",max_length=100, unique=False, blank=True, null=True)
    mine_type = models.CharField(verbose_name="نوع معدن",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سایت معدن"
        verbose_name_plural = "سایت معدن"        
        
class Mountain_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کوه"
        verbose_name_plural = "کوه"  
        
class Pile_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    Material_ty = models.CharField(verbose_name="جنس مواد",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دپو"
        verbose_name_plural = "دپو"  

class Pipe_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    ty_pipe = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    position = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    material_ty = models.CharField(verbose_name="نوع ماده",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "لوله"
        verbose_name_plural = "لوله"              

class Pipe_Lin_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    fluid_ty = models.CharField(verbose_name="نوع ماده حمل شونده",max_length=100, unique=False, blank=True, null=True)
    sze = models.CharField(verbose_name="اندازه",max_length=100, unique=False, blank=True, null=True)
    dn = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "خط لوله"
        verbose_name_plural = "خط لوله"           

class Pit_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "گودبرداری"
        verbose_name_plural = "گودبرداری"  

class Pit_Toe_Crest_Pl(LinkedToLayerTable):    
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = "لبه و پاشنه پیت"
        verbose_name_plural = "لبه و پاشنه پیت"                      
        
class Polic_S_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پاسگاه نیرو انتظامی"
        verbose_name_plural = "پاسگاه نیرو انتظامی"          

class Polic_P_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پاسگاه نیرو انتظامی"
        verbose_name_plural = "پاسگاه نیرو انتظامی"    

class Pond_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    create_ty = models.CharField(verbose_name="نحوه ایجاد",max_length=100, unique=False, blank=True, null=True)
    con_status = models.CharField(verbose_name="وضعیت تداوم",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آبگیر"
        verbose_name_plural = "آبگیر"     

class Pond_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    create_ty = models.CharField(verbose_name="نحوه ایجاد",max_length=100, unique=False, blank=True, null=True)
    con_status = models.CharField(verbose_name="وضعیت تداوم",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آبگیر"
        verbose_name_plural = "آبگیر"            
 
class Pool_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    position = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "استخر"
        verbose_name_plural = "استخر" 

class Pool_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    position = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "استخر"
        verbose_name_plural = "استخر" 
        
class Pow_Lin_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    bound = models.FloatField(verbose_name="عرض حریم",unique=False, blank=True, null=True)
    voltage = models.FloatField(verbose_name="ولتاژعبوری",unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "خط انتقال نیرو"
        verbose_name_plural = "خط انتقال نیرو"          
        
class Power_Station_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    type_pow = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت",unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نیروگاه"
        verbose_name_plural = "نیروگاه"  
        
class Pow_Pole_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تیر برق"
        verbose_name_plural = "تیر برق"                         
        
class Purification_Facilities_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت",unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تصفیه خانه"
        verbose_name_plural = "تصفیه خانه"             
        
class Puddle_W_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "گودال آب"
        verbose_name_plural = "گودال آب" 

class Qanat_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    w_cndt_ty = models.CharField(verbose_name="نوع وضعیت",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "قنات"
        verbose_name_plural = "قنات"  

class Ramp_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="عرض حریم",unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "رمپ"
        verbose_name_plural = "رمپ"                           
       

class Railway_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    bound = models.FloatField(verbose_name="عرض حریم",unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "راه آهن"
        verbose_name_plural = "راه آهن"   

class River_Pg(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    current_ty = models.CharField(verbose_name="نوع جریان",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "رودخانه"
        verbose_name_plural = "رودخانه"    

class River_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    current_ty = models.CharField(verbose_name="نوع جریان",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "رودخانه"
        verbose_name_plural = "رودخانه"       
        
        
class Road_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    sp_area_ty = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "راه"
        verbose_name_plural = "راه"

class Transport_S_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False) 

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ایستگاه حمل و نقل"
        verbose_name_plural = "ایستگاه حمل و نقل"

class Transport_S_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ایستگاه حمل و نقل"
        verbose_name_plural = "ایستگاه حمل و نقل"
        
class Sp_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    sp_area_ty = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مناطق خاص"
        verbose_name_plural = "مناطق خاص"   

class Sp_Area_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    sp_area_ty = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مناطق خاص"
        verbose_name_plural = "مناطق خاص" 
        
class Spot_H_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع ارتومتریک",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نقاط ارتفاعی"
        verbose_name_plural = "نقاط ارتفاعی"

class Spot_H_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع ارتومتریک",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نقاط ارتفاعی"
        verbose_name_plural = "نقاط ارتفاعی"    
        
class Spring_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    temperature = models.FloatField(verbose_name="دمای نسبی",unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "چشمه"
        verbose_name_plural = "چشمه"                         
        
class Stream_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آبراهه"
        verbose_name_plural = "آبراهه"       
        
class Strm_Dtc_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    create_type = models.CharField(verbose_name="نحوه ایجاد",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نهر و جوی"
        verbose_name_plural = "نهر و جوی"  
        
class Store_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    sze = models.CharField(verbose_name="اندازه",max_length=100, unique=False, blank=True, null=True)
    capacity = models.CharField(verbose_name="ظرفیت",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "انبار"
        verbose_name_plural = "انبار" 
        
class Store_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    sze = models.CharField(verbose_name="اندازه",max_length=100, unique=False, blank=True, null=True)
    capacity = models.CharField(verbose_name="ظرفیت",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "انبار"
        verbose_name_plural = "انبار"         
        
        
class Tel_Line_Pl(LinkedToLayerTable):    
    bound = models.CharField(verbose_name="عرض حریم",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "خط تلفن"
        verbose_name_plural = "خط تلفن" 

class Tel_Pole_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تیر تلفن"
        verbose_name_plural = "تیر تلفن"  
 
class Topo_Lim_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام محدوده",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده مطالعات توپوگرافی"
        verbose_name_plural = "محدوده مطالعات توپوگرافی"  
               
class Tower_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دکل برق"
        verbose_name_plural = "دکل برق"  

class Trench_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ترانشه"
        verbose_name_plural = "ترانشه"    

class Village_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    population = models.IntegerField(verbose_name="جمعیت",unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "روستا"
        verbose_name_plural = "روستا"          
        
class Village_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    population = models.IntegerField(verbose_name="جمعیت",unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "روستا"
        verbose_name_plural = "روستا" 
        
class Waste_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    type_w = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم",unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "باطله"
        verbose_name_plural = "باطله" 
        
class Warehouse_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    user_status = models.CharField(verbose_name="وضعیت کاربری",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محوطه انبار"
        verbose_name_plural = "محوطه انبار"         
        
        
class Wat_Cour_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آبریز"
        verbose_name_plural = "آبریز"  
        
class Water_W_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    w_cndt_ty = models.CharField(verbose_name="نوع وضعیت",max_length=100, unique=False, blank=True, null=True)
    w_type = models.CharField(verbose_name="نوع چاه",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = " چاه آب"
        verbose_name_plural = " چاه آب"

class Oil_W_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    w_cndt_ty = models.CharField(verbose_name="نوع وضعیت",max_length=100, unique=False, blank=True, null=True)
    w_type = models.CharField(verbose_name="نوع چاه",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = " چاه نفت"
        verbose_name_plural = " چاه نفت"

class Wall_Pl(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دیوار"
        verbose_name_plural = "دیوار" 

class Other_Place_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    position = models.CharField(verbose_name="موقعیت",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سایر اماکن"
        verbose_name_plural = "سایر اماکن"

class Other_Place_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    position = models.CharField(verbose_name="موقعیت",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سایر اماکن"
        verbose_name_plural = "سایر اماکن" 

class Swamp_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = " باتلاق"
        verbose_name_plural = " باتلاق" 

class Shore_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = " ساحل"
        verbose_name_plural = " ساحل"

class Culvert_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زیرآبگذر یا کالورت"
        verbose_name_plural = "زیرآبگذر یا کالورت"

class Culvert_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زیرآبگذر یا کالورت"
        verbose_name_plural = "زیرآبگذر یا کالورت"


class Fire_Station_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ایستگاه آتش نشانی"
        verbose_name_plural = "ایستگاه آتش نشانی"

class Fire_Station_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ایستگاه آتش نشانی"
        verbose_name_plural = "ایستگاه آتش نشانی"

class Clif_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "صخره"
        verbose_name_plural = "صخره"

class Clif_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "صخره"
        verbose_name_plural = "صخره"

class Land_Capture_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زمین تصرفی"
        verbose_name_plural = "زمین تصرفی"  

class Well_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True) 
    depth = models.FloatField(verbose_name="عمق",unique=False, blank=True, null=True) 
    cross_sec = models.FloatField(verbose_name="اختلاف متوسط",unique=False, blank=True, null=True) 
    length_sec = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True) 
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True) 
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "چاه"
        verbose_name_plural = "چاه"  

class Gate_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=250, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "در ورودی یا دریچه"
        verbose_name_plural = "در ورودی یا دریچه"

class Gaz_OR_Water_Station_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=250, unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="گنجایش",unique=False, blank=True, null=True) 
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ایستگاه گاز یا آب"
        verbose_name_plural = "ایستگاه گاز یا آب"

class Gaz_OR_Water_Station_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=250, unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="گنجایش",unique=False, blank=True, null=True) 
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ایستگاه گاز یا آب"
        verbose_name_plural = "ایستگاه گاز یا آب"

class Waterfall_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آبشار"
        verbose_name_plural = "آبشار"

class Waterfall_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آبشار"
        verbose_name_plural = "آبشار"

class Waterfall_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آبشار"
        verbose_name_plural = "آبشار"

class Gate_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=250, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "در ورودی یا دریچه"
        verbose_name_plural = "در ورودی یا دریچه"

class Camping_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محل استراحت"
        verbose_name_plural = "محل استراحت"  

class Qanat_Pt(LinkedToLayerTable):    
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    w_cndt_ty = models.CharField(verbose_name="نوع وضعیت",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "قنات"
        verbose_name_plural = "قنات"  

class Fac_Dump_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    ore_type = models.CharField(verbose_name="نوع ماده معدني",max_length=100, unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم ماده معدنی",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دامپ کارخانه"
        verbose_name_plural = "دامپ کارخانه"    

class Fac_Dump_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    ore_type = models.CharField(verbose_name="نوع ماده معدني",max_length=100, unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم ماده معدنی",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دامپ کارخانه"
        verbose_name_plural = "دامپ کارخانه"

class Fac_Dump_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    ore_type = models.CharField(verbose_name="نوع ماده معدني",max_length=100, unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم ماده معدنی",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دامپ کارخانه"
        verbose_name_plural = "دامپ کارخانه"    

class Borrow_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "منابع قرضه"
        verbose_name_plural = "منابع قرضه"  

class Borrow_Area_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "منابع قرضه"
        verbose_name_plural = "منابع قرضه"   

class Optical_Fiber_Line_Pl(LinkedToLayerTable):
    bound = models.CharField(verbose_name="عرض حریم",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فیبر نوری"
        verbose_name_plural = "فیبر نوری" 

class Transfer_Power_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ترانسفر برق"
        verbose_name_plural = "ترانسفر برق" 

class Transfer_Power_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ترانسفر برق"
        verbose_name_plural = "ترانسفر برق" 

class Other_Place_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    position = models.CharField(verbose_name="موقعیت",max_length=250, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سایر اماکن"
        verbose_name_plural = "سایر اماکن"

class Pile_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    Material_ty = models.CharField(verbose_name="جنس مواد",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دپو"
        verbose_name_plural = "دپو"  

class Gate_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)

    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "در ورودی یا دریچه"
        verbose_name_plural = "در ورودی یا دریچه"

class Lagoon_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تالاب"
        verbose_name_plural = "تالاب"

class Forest_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "جنگل"
        verbose_name_plural = "جنگل"

class GazOrWaterOrPowerMeter_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=250, unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کنتور برق آب گاز"
        verbose_name_plural = "کنتور برق آب گاز"

class GazOrWaterOrPowerMeter_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=250, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=250, unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False) 

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کنتور برق آب گاز"
        verbose_name_plural = "کنتور برق آب گاز"