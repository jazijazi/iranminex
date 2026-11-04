from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable

class Fault_Gph_sec_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    l_gph_sec_id = models.CharField(verbose_name="شناسه مقطع ژئوفیزیک",max_length=100, unique=False, blank=True, null=True)
    type_fault = models.CharField(verbose_name="نوع گسل",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "گسل ژئوفيزيک در مقطع"
        verbose_name_plural = "گسل ژئوفيزيک در مقطع"          
                
class Gph_Ano_S_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    priority = models.CharField(verbose_name="اولویت",max_length=100, unique=False, blank=True, null=True)
    l_gph_sec_id = models.CharField(verbose_name="شناسه مقطع ژئوفیزیک",max_length=100, unique=False, blank=True, null=True)
    det_method = models.CharField(verbose_name="روش تعیین",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "زون ناهنجاري ژئوفيزيك در ‌مقطع"
        verbose_name_plural = "زون ناهنجاري ژئوفيزيك در ‌مقطع"  
                
class Gph_Sec_P_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    l_gph_sec_id = models.CharField(verbose_name="شناسه مقطع ژئوفیزیک",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پروفيل مقطع ژئوفيزيک"
        verbose_name_plural = "پروفيل مقطع ژئوفيزيک" 

class Grav_Ano_S_Pg(LinkedToLayerTable):
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    l_gph_sec_id = models.CharField(verbose_name="شناسه مقطع ژئوفیزیک",max_length=100, unique=False, blank=True, null=True)
    lower_lim = models.FloatField(verbose_name="حد پایین",unique=False, blank=True, null=True)
    upper_lim = models.FloatField(verbose_name="حد بالا",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = "زون ناهنجاري در مقطع"
        verbose_name_plural = "زون ناهنجاري در مقطع"          

class IP_Ano_S_Pg(LinkedToLayerTable):
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    l_gph_sec_id = models.CharField(verbose_name="شناسه مقطع ژئوفیزیک",max_length=100, unique=False, blank=True, null=True)
    lower_lim = models.FloatField(verbose_name="حد پایین",unique=False, blank=True, null=True)
    upper_lim = models.FloatField(verbose_name="حد بالا",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = " زون ناهنجاري پولاريزاسيون القايي در مقطع"
        verbose_name_plural = " زون ناهنجاري پولاريزاسيون القايي در مقطع"     

class Mag_Ano_S_Pg(LinkedToLayerTable):
    typ = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    l_gph_sec_id = models.CharField(verbose_name="شناسه مقطع ژئوفیزیک",max_length=100, unique=False, blank=True, null=True)
    lower_lim = models.FloatField(verbose_name="حد پایین",unique=False, blank=True, null=True)
    upper_lim = models.FloatField(verbose_name="حد بالا",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = "زون ناهنجاري مغناطيسي در مقطع"
        verbose_name_plural = "زون ناهنجاري مغناطيسي در مقطع"      

class Rck_Typ_Gph_S_Pg(LinkedToLayerTable):
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
        verbose_name = "تيپ سنگ شناسي مقطع ژئوفيزيک"
        verbose_name_plural = "تيپ سنگ شناسي مقطع ژئوفيزيک"