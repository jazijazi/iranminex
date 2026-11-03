from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable


class Extraction_Block_Pg(LinkedToLayerTable):
    name_blast        = models.CharField(verbose_name="شناسه هر مرحله انفجار",max_length=200 , unique=False,blank=True,null=True)
    blast_n           = models.FloatField(verbose_name="تعداد اتشباری" , unique=False,blank=True,null=True)
    hole_n            = models.FloatField(verbose_name="تعداد چال" , unique=False,blank=True,null=True)
    value             = models.FloatField(verbose_name="مقدار مواد منفجره مصرفی" , unique=False,blank=True,null=True)
    date              = models.CharField(verbose_name="تاریخ " ,max_length=250, unique=False,blank=True,null=True)
    tonag             = models.FloatField(verbose_name="تناژ عملکرد انفجار" , unique=False,blank=True,null=True)
    special_expense   = models.FloatField(verbose_name="خرج ویژه" , unique=False,blank=True,null=True)
    w_density         = models.FloatField(verbose_name="وزن مخصوص سنگ" , unique=False,blank=True,null=True)
    rock_density      = models.FloatField(verbose_name="وزن مخصوص باطله" , unique=False,blank=True,null=True)
    comment           = models.CharField(verbose_name="توضیحات " ,max_length=250, unique=False,blank=True,null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name_blast
    class Meta:
        verbose_name = "بلوک استخراج"
        verbose_name_plural = "بلوک استخراج"

class Extraction_Bench_Mark_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره" ,max_length=250, unique=False,blank=True,null=True)
    typ = models.CharField(verbose_name="نوع" ,max_length=250, unique=False,blank=True,null=True)
    elevation = models.FloatField(verbose_name="ارتفاع" , unique=False,blank=True,null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ایستگاه نقشه برداری"
        verbose_name_plural = "ایستگاه نقشه برداری"

class Extraction_Mine_Dump_Pg(LinkedToLayerTable):
    depo_n        = models.CharField(verbose_name="شناسه  هر دپو" ,max_length=250, unique=False,blank=True,null=True)
    volume_mine   = models.FloatField(verbose_name="حجم باطله" , unique=False,blank=True,null=True)
    survey_date   = models.CharField(verbose_name="تاریخ نقشه برداری" ,max_length=250, unique=False,blank=True,null=True)
    comment       = models.CharField(verbose_name="توضیحات" ,max_length=250, unique=False,blank=True,null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.depo_n
    class Meta:
        verbose_name = "دامپ ماده معدنی"
        verbose_name_plural = "دامپ ماده معدنی"

class Extraction_Mine_Dump_Pl(LinkedToLayerTable):
    depo_n        = models.CharField(verbose_name="شناسه  هر دپو" ,max_length=250, unique=False,blank=True,null=True)
    volume_mine   = models.FloatField(verbose_name="حجم باطله" , unique=False,blank=True,null=True)
    survey_date   = models.CharField(verbose_name="تاریخ نقشه برداری" ,max_length=250, unique=False,blank=True,null=True)
    comment       = models.CharField(verbose_name="توضیحات" ,max_length=250, unique=False,blank=True,null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 

    def __str__(self):
        return self.depo_n
    class Meta:
        verbose_name = "دامپ ماده معدنی"
        verbose_name_plural = "دامپ ماده معدنی"

class Extraction_Mine_Dump_Pt(LinkedToLayerTable):
    depo_n        = models.CharField(verbose_name="شناسه  هر دپو" ,max_length=250, unique=False,blank=True,null=True)
    volume_mine   = models.FloatField(verbose_name="حجم باطله" , unique=False,blank=True,null=True)
    survey_date   = models.CharField(verbose_name="تاریخ نقشه برداری" ,max_length=250, unique=False,blank=True,null=True)
    comment       = models.CharField(verbose_name="توضیحات" ,max_length=250, unique=False,blank=True,null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.depo_n
    class Meta:
        verbose_name = "دامپ ماده معدنی"
        verbose_name_plural = "دامپ ماده معدنی"

class Extraction_Operation_Drilling_Pg(LinkedToLayerTable):
    name_drill    = models.CharField(verbose_name="شناسه حفاری" ,max_length=250, unique=False,blank=True,null=True)
    method        = models.CharField(verbose_name="روش حفاری" ,max_length=250, unique=False,blank=True,null=True)
    drilling_type = models.CharField(verbose_name="نوع حفاری" ,max_length=250, unique=False,blank=True,null=True)
    excavator     = models.CharField(verbose_name="مجری حفاری" ,max_length=250, unique=False,blank=True,null=True)
    depth         = models.FloatField(verbose_name="عمق" , unique=False,blank=True,null=True)
    diameter      = models.FloatField(verbose_name="قطر" , unique=False,blank=True,null=True)
    dip           = models.FloatField(verbose_name="شیب حفاری" , unique=False,blank=True,null=True)
    drilling_cost = models.FloatField(verbose_name="هزینه حفاری" , unique=False,blank=True,null=True)
    drilling_date = models.FloatField(verbose_name="تاریخ انجام حفاری" , unique=False,blank=True,null=True)
    volume        = models.FloatField(verbose_name="حجم استخراج" , unique=False,blank=True,null=True)
    w_Density     = models.FloatField(verbose_name="وزن مخصوص باطله" , unique=False,blank=True,null=True)
    rock_density  = models.FloatField(verbose_name="وزن مخصوص سنگ " , unique=False,blank=True,null=True)
    comment       = models.CharField(verbose_name="توضیحات " ,max_length=250, unique=False,blank=True,null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name_drill
    class Meta:
        verbose_name = "عملیات اجرای حفاری"
        verbose_name_plural = "عملیات اجرای حفاری"

class Extraction_Operation_Drilling_Pl(LinkedToLayerTable):
    name_drill    = models.CharField(verbose_name="شناسه حفاری" ,max_length=250, unique=False,blank=True,null=True)
    method        = models.CharField(verbose_name="روش حفاری" ,max_length=250, unique=False,blank=True,null=True)
    drilling_type = models.CharField(verbose_name="نوع حفاری" ,max_length=250, unique=False,blank=True,null=True)
    excavator     = models.CharField(verbose_name="مجری حفاری" ,max_length=250, unique=False,blank=True,null=True)
    depth         = models.FloatField(verbose_name="عمق" , unique=False,blank=True,null=True)
    diameter      = models.FloatField(verbose_name="قطر" , unique=False,blank=True,null=True)
    dip           = models.FloatField(verbose_name="شیب حفاری" , unique=False,blank=True,null=True)
    drilling_cost = models.FloatField(verbose_name="هزینه حفاری" , unique=False,blank=True,null=True)
    drilling_date = models.FloatField(verbose_name="تاریخ انجام حفاری" , unique=False,blank=True,null=True)
    volume        = models.FloatField(verbose_name="حجم استخراج" , unique=False,blank=True,null=True)
    w_Density     = models.FloatField(verbose_name="وزن مخصوص باطله" , unique=False,blank=True,null=True)
    rock_density  = models.FloatField(verbose_name="وزن مخصوص سنگ " , unique=False,blank=True,null=True)
    comment       = models.CharField(verbose_name="توضیحات " ,max_length=250, unique=False,blank=True,null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    

    def __str__(self):
        return self.name_drill
    class Meta:
        verbose_name = "عملیات اجرای حفاری"
        verbose_name_plural = "عملیات اجرای حفاری"

class Extraction_Operation_Drilling_Pt(LinkedToLayerTable):
    name_drill    = models.CharField(verbose_name="شناسه حفاری" ,max_length=250, unique=False,blank=True,null=True)
    method        = models.CharField(verbose_name="روش حفاری" ,max_length=250, unique=False,blank=True,null=True)
    drilling_type = models.CharField(verbose_name="نوع حفاری" ,max_length=250, unique=False,blank=True,null=True)
    excavator     = models.CharField(verbose_name="مجری حفاری" ,max_length=250, unique=False,blank=True,null=True)
    depth         = models.FloatField(verbose_name="عمق" , unique=False,blank=True,null=True)
    diameter      = models.FloatField(verbose_name="قطر" , unique=False,blank=True,null=True)
    dip           = models.FloatField(verbose_name="شیب حفاری" , unique=False,blank=True,null=True)
    drilling_cost = models.FloatField(verbose_name="هزینه حفاری" , unique=False,blank=True,null=True)
    drilling_date = models.FloatField(verbose_name="تاریخ انجام حفاری" , unique=False,blank=True,null=True)
    volume        = models.FloatField(verbose_name="حجم استخراج" , unique=False,blank=True,null=True)
    w_Density     = models.FloatField(verbose_name="وزن مخصوص باطله" , unique=False,blank=True,null=True)
    rock_density  = models.FloatField(verbose_name="وزن مخصوص سنگ " , unique=False,blank=True,null=True)
    comment       = models.CharField(verbose_name="توضیحات " ,max_length=250, unique=False,blank=True,null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)


    def __str__(self):
        return self.name_drill
    class Meta:
        verbose_name = "عملیات اجرای حفاری"
        verbose_name_plural = "عملیات اجرای حفاری"