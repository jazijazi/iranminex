from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable

class Alteration_RS_Pg(LinkedToLayerTable):
    sat_sensor_name = models.CharField(verbose_name="نام سنجده",max_length=100, unique=False, blank=True, null=True)
    alt_name = models.CharField(verbose_name="نام دگرسانی",max_length=100, unique=False, blank=True, null=True)
    comment_fa = models.CharField(verbose_name="توضیحات فارسی",max_length=250, unique=False, blank=True, null=True)
    comment_en = models.CharField(verbose_name="توضیحات لاتین",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.sat_sensor_name
    class Meta:
        verbose_name = "محدوده دگرسان دورسنجي"
        verbose_name_plural = "محدوده دگرسان دورسنجي"  

class Fault_RS_Pl(LinkedToLayerTable):
    sat_sensor_name = models.CharField(verbose_name="نام سنجنده",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.sat_sensor_name
    class Meta:
        verbose_name = "گسل حاصل از دورسنجی"
        verbose_name_plural = "گسل حاصل از دورسنجی"  
        
class Lineament_RS_Pl(LinkedToLayerTable):
    sat_sensor_name = models.CharField(verbose_name="نام سنجنده",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.sat_sensor_name
    class Meta:
        verbose_name = "خطواره حاصل از دورسنجي"
        verbose_name_plural = "خطواره حاصل از دورسنجي"   

class Rck_Typ_RS_Pg(LinkedToLayerTable):
    sat_sensor_name = models.CharField(verbose_name="نام سنجده",max_length=100, unique=False, blank=True, null=True)
    geo_unit = models.CharField(verbose_name="نام لایه به اختصار",max_length=100, unique=False, blank=True, null=True)
    formation = models.CharField(verbose_name="سازند",max_length=100, unique=False, blank=True, null=True)
    era = models.CharField(verbose_name="دوران",max_length=100, unique=False, blank=True, null=True)
    period = models.CharField(verbose_name="دوره",max_length=100, unique=False, blank=True, null=True)
    origin = models.CharField(verbose_name="خاستگاه",max_length=100, unique=False, blank=True, null=True)
    comment_fa = models.CharField(verbose_name="توضیحات فارسی",max_length=250, unique=False, blank=True, null=True)
    comment_en = models.CharField(verbose_name="توضیحات انگلیسی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.sat_sensor_name
    class Meta:
        verbose_name = "سنگ شناسي حاصل از دورسنجي"
        verbose_name_plural = "سنگ شناسي حاصل از دورسنجي"  

class Ring_Struct_RS_Pl(LinkedToLayerTable):
    sat_sensor_name = models.CharField(verbose_name="نام سنجنده",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.sat_sensor_name
    class Meta:
        verbose_name = "ساختار حلقوي حاصل از دورسنجي"
        verbose_name_plural = "ساختار حلقوي حاصل از دورسنجي"   

class RS_Ano_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    priority = models.CharField(verbose_name="اولویت",max_length=100, unique=False, blank=True, null=True)
    det_method = models.CharField(verbose_name="روش تعیین",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده اميد بخش دور سنجي"
        verbose_name_plural = "محدوده اميد بخش دور سنجي"  
        
class RS_Lim_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده مطالعات دورسنجي"
        verbose_name_plural = "محدوده مطالعات دورسنجي"     

class Sat_Image_Pg(LinkedToLayerTable):
    sat_sensor_name = models.CharField(verbose_name="نام سنجده",max_length=100, unique=False, blank=True, null=True)
    img_aquire_time = models.DateField(verbose_name="تاریخ اخذ تصویر",auto_now=False,auto_now_add=False,null=True,blank=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "اطلاعات تصاوير ماهواره اي"
        verbose_name_plural = "اطلاعات تصاوير ماهواره اي" 