from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable


class Nut_Res_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    exp_stage = models.CharField(verbose_name="مرحله اکتشافی",max_length=100, unique=False, blank=True, null=True)
    number = models.FloatField(verbose_name="شماره ثبت",unique=False, blank=True, null=True)
    date = models.DateField(verbose_name="تاریخ",auto_now=False,auto_now_add=False,null=True,blank=True)
    license_no = models.CharField(verbose_name="شماره مجوز",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده های دارای مجوز منابع طبیعی"
        verbose_name_plural = "محدوده های دارای مجوز منابع طبیعی" 
        
class Envi_Per_Area_Pg(LinkedToLayerTable):
    area_ty = models.CharField(verbose_name="نوع منطقه",max_length=100, unique=False, blank=True, null=True)
    plan_title = models.CharField(verbose_name="عنوان طرح",max_length=100, unique=False, blank=True, null=True)
    proj_title = models.CharField(verbose_name="عنوان پروژه",max_length=100, unique=False, blank=True, null=True)
    scale = models.FloatField(verbose_name="مقیاس",unique=False, blank=True, null=True)
    en_date = models.DateField(verbose_name="تاریخ صدور مجوز زیست محیطی",auto_now=False,auto_now_add=False,null=True,blank=True)
    exp_data = models.DateField(verbose_name="تاریخ انقضا مجوز زیست محیطی",auto_now=False,auto_now_add=False,null=True,blank=True)
    ext_data = models.DateField(verbose_name="تاریخ تمدید مجوز زیست محیطی",auto_now=False,auto_now_add=False,null=True,blank=True)
    max_depth = models.FloatField(verbose_name="حداکثر عمق مجاز بهره برداری (معدن روباز)",unique=False, blank=True, null=True)
    license_num = models.CharField(verbose_name="شماره مجوز",max_length=100, unique=False, blank=True, null=True)
    license_type = models.CharField(verbose_name="نوع مجوز",max_length=100, unique=False, blank=True, null=True)
    issue_date = models.DateField(verbose_name="تاریخ صدور",auto_now=False,auto_now_add=False,null=True,blank=True)
    licen_credit = models.FloatField(verbose_name="اعتبار مجوز",unique=False, blank=True, null=True)
    activ_ty = models.CharField(verbose_name="نوع فعالیت معدنی",max_length=100, unique=False, blank=True, null=True)
    extrac_cap = models.FloatField(verbose_name="ظرفیت استخراج",unique=False, blank=True, null=True)
    mineral_ty = models.CharField(verbose_name="نوع ماده معدنی",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.area_ty
    class Meta:
        verbose_name = "محدوده‌های دارای مجوز زیست محیطی"
        verbose_name_plural = "محدوده‌های دارای مجوز زیست محیطی"         

class Env_Protection_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    epareakind = models.CharField(verbose_name="نوع",max_length=100, unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مناطق حفاظت شده محیط زیست"
        verbose_name_plural = "مناطق حفاظت شده محیط زیست"    

class Explor_Per_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    owner_name = models.CharField(verbose_name="نام مالک",max_length=100, unique=False, blank=True, null=True)
    doc_no = models.CharField(verbose_name="شماره پروانه",max_length=100, unique=False, blank=True, null=True)
    mineral_ty = models.CharField(verbose_name="نوع ذخیره معدنی",max_length=100, unique=False, blank=True, null=True)
    minera_vol = models.FloatField(verbose_name="ذخیره ماده معدنی",unique=False, blank=True, null=True)
    doc_date = models.DateField(verbose_name="تاریخ صدور پروانه",auto_now=False,auto_now_add=False,null=True,blank=True)
    exp_date = models.DateField(verbose_name="تاریخ انقضا",auto_now=False,auto_now_add=False,null=True,blank=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده های دارای پروانه اکتشاف"
        verbose_name_plural = "محدوده های دارای پروانه اکتشاف"     
        
class Exp_Agr_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    owner_name = models.CharField(verbose_name="شماره گواهی",max_length=100, unique=False, blank=True, null=True)
    doc_no = models.CharField(verbose_name="نوع ذخیره معدنی",max_length=100, unique=False, blank=True, null=True)
    mineral_ty = models.CharField(verbose_name="میزان ذخیره ماده معدنی به تن",max_length=100, unique=False, blank=True, null=True)
    minera_vol = models.FloatField(verbose_name="نام مالک",unique=False, blank=True, null=True)
    doc_date = models.DateField(verbose_name="تاریخ صدور گواهی",auto_now=False,auto_now_add=False,null=True,blank=True)
    exp_date = models.DateField(verbose_name="تاریخ انقضا",auto_now=False,auto_now_add=False,null=True,blank=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده های دارای گواهی کشف"
        verbose_name_plural = "محدوده های دارای گواهی کشف"     
        
class Exploit_Per_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    owner_name = models.CharField(verbose_name="نام مالک",max_length=100, unique=False, blank=True, null=True)
    mineral_ty = models.CharField(verbose_name="نوع ذخیره معدنی",max_length=100, unique=False, blank=True, null=True)
    ore_grade = models.FloatField(verbose_name="عیار متوسط",unique=False, blank=True, null=True)
    ore_prob = models.FloatField(verbose_name="میزان ذخیره احتمالی",unique=False, blank=True, null=True)
    ore_prov = models.FloatField(verbose_name="میزان ذخیره قطعی",unique=False, blank=True, null=True)
    doc_no = models.CharField(verbose_name="شماره پروانه",max_length=100, unique=False, blank=True, null=True)
    doc_date = models.DateField(verbose_name="تاریخ صدور پروانه",auto_now=False,auto_now_add=False,null=True,blank=True)
    exp_date = models.DateField(verbose_name="تاریخ انقضا",auto_now=False,auto_now_add=False,null=True,blank=True)
    expliotdep = models.FloatField(verbose_name="میزان بهره برداری ",unique=False, blank=True, null=True)
    extrac_sys = models.CharField(verbose_name="سیستم استخراج",max_length=100, unique=False, blank=True, null=True)
    amount_inv = models.FloatField(verbose_name="میزان سرمایه گذاری",unique=False, blank=True, null=True)
    employment = models.FloatField(verbose_name="اشتغال",unique=False, blank=True, null=True)
    pile = models.FloatField(verbose_name="میزان دپو",unique=False, blank=True, null=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده های دارای پروانه بهره برداری"
        verbose_name_plural = "محدوده های دارای پروانه بهره برداری"

class Exp_Req_Area_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    owner_name = models.CharField(verbose_name="نام مالک",max_length=100, unique=False, blank=True, null=True)
    doc_no = models.CharField(verbose_name="شماره پروانه",max_length=100, unique=False, blank=True, null=True)
    mineral_ty = models.CharField(verbose_name="نوع ذخیره معدنی",max_length=100, unique=False, blank=True, null=True)
    minera_vol = models.FloatField(verbose_name="ذخیره ماده معدنی",unique=False, blank=True, null=True)
    doc_date = models.DateField(verbose_name="تاریخ صدور پروانه",auto_now=False,auto_now_add=False,null=True,blank=True)
    exp_date = models.DateField(verbose_name="تاریخ انقضا",auto_now=False,auto_now_add=False,null=True,blank=True)
    comment = models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده های دارای درخواست اکتشاف"
        verbose_name_plural = "محدوده های دارای درخواست اکتشاف"  

class Area_License_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام",max_length=100, unique=False, blank=True, null=True)
    number = models.FloatField(verbose_name="شماره ثبت",unique=False, blank=True, null=True)
    date = models.DateField(verbose_name="تاریخ",auto_now=False,auto_now_add=False,null=True,blank=True)
    license_no = models.CharField(verbose_name="شماره مجوز",max_length=100, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "محدوده های دارای مجوز"
        verbose_name_plural = "محدوده های دارای مجوز" 