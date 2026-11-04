from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable

class Automation_System_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیستم اتوماسیون"
        verbose_name_plural = "سیستم اتوماسیون"
        
class Automation_System_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیستم اتوماسیون"
        verbose_name_plural = "سیستم اتوماسیون"        
   
   
class Agitator_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "همزن"
        verbose_name_plural = "همزن"
        
class Agitator_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "همزن"
        verbose_name_plural = "همزن"        
        
class Air_Receiverr_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "رسیور هوا"
        verbose_name_plural = "رسیور هوا"
        
class Air_Receiver_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "رسیور هوا"
        verbose_name_plural = "رسیور هوا"              

class Air_Lift_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ایرلیفت"
        verbose_name_plural = "ایرلیفت"
        
class Air_Lift_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ایرلیفت"
        verbose_name_plural = "ایرلیفت"              

class Boiler_House_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرتت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شوفاژخانه"
        verbose_name_plural = "شوفاژخانه"
        
class Boiler_House_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شوفاژخانه"
        verbose_name_plural = "شوفاژخانه" 

class Bonker_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "بونکر"
        verbose_name_plural = "بونکر"
        
class Bonker_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "بونکر"
        verbose_name_plural = "بونکر"  
        
class Cable_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    voltage = models.FloatField(verbose_name="ولتاژ",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق کار",unique=False, blank=True, null=True)
    sze = models.CharField(verbose_name="اندازه",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کابل"
        verbose_name_plural = "کابل"               

class Compressor_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کمپرسور"
        verbose_name_plural = "کمپرسور"
        
class Compressor_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کمپرسور"
        verbose_name_plural = "کمپرسور"  
        
class Crusher_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سنگ شکن"
        verbose_name_plural = "سنگ شکن"
        
class Crusher_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سنگ شکن"
        verbose_name_plural = "سنگ شکن"  

class Conveyor_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نوار نقاله"
        verbose_name_plural = "نوار نقاله"
        
class Conveyor_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نوار نقاله"
        verbose_name_plural = "نوار نقاله"                                      
        
class Conveyor_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "نوار نقاله"
        verbose_name_plural = "نوار نقاله"  

class Derrick_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "جرثقیل سقفی"
        verbose_name_plural = "جرثقیل سقفی"
        
class Derrick_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "جرثقیل سقفی"
        verbose_name_plural = "جرثقیل سقفی"  
        
class Dost_Kalkator_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "داست كالكتور"
        verbose_name_plural = "داست كالكتور"
        
class Dost_Kalkator_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "داست كالكتور"
        verbose_name_plural = "داست كالكتور"                                      
        

class Dryer_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "خشک کن"
        verbose_name_plural = "خشک کن"
        
class Dryer_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "خشک کن"
        verbose_name_plural = "خشک کن"                              
        
class ElectricityStation_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    input_vol = models.FloatField(verbose_name="ولتاژ ورودی",unique=False, blank=True, null=True)
    output_vol = models.FloatField(verbose_name="ولتاژ خروجی",unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پست برق"
        verbose_name_plural = "پست برق"
        
class ElectricityStation_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    input_vol = models.FloatField(verbose_name="ولتاژ ورودی",unique=False, blank=True, null=True)
    output_vol = models.FloatField(verbose_name="ولتاژ خروجی",unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پست برق"
        verbose_name_plural = "پست برق" 
        
class Electrowinning_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = " الکترووینینگ"
        verbose_name_plural = " الکترووینینگ"
        
class Electrowinning_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "الکترووینینگ"
        verbose_name_plural = "الکترووینینگ"                    

class Electrowinning_Cell_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سلول الکترووینینگ"
        verbose_name_plural = "سلول الکترووینینگ"
        
class Electrowinning_Cell_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سلول الکترووینینگ"
        verbose_name_plural = "سلول الکترووینینگ" 

class Feeder_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فیدر"
        verbose_name_plural = "فیدر"
        
class Feeder_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فیدر"
        verbose_name_plural = "فیدر" 
        
class Filter_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.FloatField(verbose_name="سال ساخت",unique=False, blank=True, null=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فیلتر"
        verbose_name_plural = "فیلتر"
        
class Filter_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فیلتر"
        verbose_name_plural = "فیلتر"                                      

class Furnace_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کوره"
        verbose_name_plural = "کوره"
        
class Furnace_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کوره"
        verbose_name_plural = "کوره" 

class Valve_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    sze = models.FloatField(verbose_name="اندازه",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دریچه یا شیر فلکه"
        verbose_name_plural = "دریچه یا شیر فلکه"
        
class Valve_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    sze = models.FloatField(verbose_name="اندزه",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دریچه یا شیر فلکه"
        verbose_name_plural = "دریچه یا شیر فلکه"                                      

class Heat_Exchanger_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مبدل های حرارتی"
        verbose_name_plural = "مبدل های حرارتی"
        
class Heat_Exchanger_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مبدل های حرارتی"
        verbose_name_plural = "مبدل های حرارتی"    
        
class Heating_system_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیستم های گرمایشی"
        verbose_name_plural = "سیستم های گرمایشی"
        
class Heating_system_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیستم های گرمایشی"
        verbose_name_plural = "سیستم های گرمایشی"                               

class High_Voltage_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "های ولتاژ"
        verbose_name_plural = "های ولتاژ"
        
class High_Voltage_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "های ولتاژ"
        verbose_name_plural = "های ولتاژ"     

class Hydrocarbon_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "هيدروکربن"
        verbose_name_plural = "هيدروکربن"
        
class Hydrocarbon_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "هيدروکربن"
        verbose_name_plural = "هيدروکربن"  

class Magnet_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مگنت"
        verbose_name_plural = "مگنت"
        
class Magnet_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مگنت"
        verbose_name_plural = "مگنت"                        
        

class Manhole_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "منهول"
        verbose_name_plural = "منهول"
        
class Manhole_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "منهول"
        verbose_name_plural = "منهول"                              

class Mill_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آسیاب"
        verbose_name_plural = "آسیاب"
        
class Mill_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آسیاب"
        verbose_name_plural = "آسیاب"  

class Other_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سایر تجهیزات"
        verbose_name_plural = "سایر تجهیزات"
        
class Other_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سایر تجهیزات"
        verbose_name_plural = "سایر تجهیزات"          

class Pump_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پمپ"
        verbose_name_plural = "پمپ"
        
class Pump_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پمپ"
        verbose_name_plural = "پمپ"  

class Sump_pump_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سامپ پمپ"
        verbose_name_plural = "سامپ پمپ"
        
class Sump_pump_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سامپ پمپ"
        verbose_name_plural = "سامپ پمپ"          

class Silo_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیلو"
        verbose_name_plural = "سیلو"
        
class Silo_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیلو"
        verbose_name_plural = "سیلو"                
        
class Safety_showers_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دوش های ایمنی"
        verbose_name_plural = "دوش های ایمنی"
        
class Safety_Showers_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دوش های ایمنی"
        verbose_name_plural = "دوش های ایمنی"                                            

class Screen_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سرند"
        verbose_name_plural = "سرند"
        
class Screen_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سرند"
        verbose_name_plural = "سرند"   
        
class Shoot_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شوت"
        verbose_name_plural = "شوت"
        
class Shoot_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شوت"
        verbose_name_plural = "شوت"  

class Storage_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مخزن"
        verbose_name_plural = "مخزن"
        
class Storage_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "مخزن"
        verbose_name_plural = "مخزن"  

class Rotary_Voloum_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "روتاري ولو"
        verbose_name_plural = "روتاري ولو"
        
class Rotary_Voloum_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "روتاري ولو"
        verbose_name_plural = "روتاري ولو"  

class Tank_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تانک"
        verbose_name_plural = "تانک"
        
class Tank_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تانک"
        verbose_name_plural = "تانک"          
        
class Trans_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ترانس"
        verbose_name_plural = "ترانس"
        
class Trans_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ترانس"
        verbose_name_plural = "ترانس"      

class Tikner_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تیکنر"
        verbose_name_plural = "تیکنر"
        
class Tikner_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تیکنر"
        verbose_name_plural = "تیکنر"  

class Vibrator_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ویبراتور"
        verbose_name_plural = "ویبراتور"
        
class Vibrator_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ویبراتور"
        verbose_name_plural = "ویبراتور"  
        
class Weight_Gauge_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "وزن سنج"
        verbose_name_plural = "وزن سنج"
        
class Weight_Gauge_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "وزن سنج"
        verbose_name_plural = "وزن سنج"  

class Weigh_Bridge_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "باسکول"
        verbose_name_plural = "باسکول"
        
class Weigh_Bridge_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "باسکول"
        verbose_name_plural = "باسکول"

class Tap_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شیر آب"
        verbose_name_plural = "شیر آب"

class Tap_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شیر آب"
        verbose_name_plural = "شیر آب"

class Chiler_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "چیلر"
        verbose_name_plural = "چیلر"
        
class Chiler_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "چیلر"
        verbose_name_plural = "چیلر"

class Tower_Separation_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "برج جدایش"
        verbose_name_plural = "برج جدایش"

class Tower_Separation_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "برج جدایش"
        verbose_name_plural = "برج جدایش"

class Pool_Eq_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "استخر یا حوضچه"
        verbose_name_plural = "استخر یا حوضچه"
class Pool_Eq_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "استخر یا حوضچه"
        verbose_name_plural = "استخر یا حوضچه"

class Grid_Stone_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تاسیسات میز خاکشویی"
        verbose_name_plural = "تاسیسات میز خاکشویی"
class Grid_Stone_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تاسیسات میز خاکشویی"
        verbose_name_plural = "تاسیسات میز خاکشویی"

class Ventilator_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تهویه"
        verbose_name_plural = "تهویه"

class Ventilator_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تهویه"
        verbose_name_plural = "تهویه"

class Ventilator_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "تهویه"
        verbose_name_plural = "تهویه"

class Elevator_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آسانسور"
        verbose_name_plural = "آسانسور"

class Elevator_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آسانسور"
        verbose_name_plural = "آسانسور"

class Elevator_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آسانسور"
        verbose_name_plural = "آسانسور"

class Unit_Pg(LinkedToLayerTable):
    name_en = models.CharField(verbose_name="نام فارسی",max_length=100, unique=False, blank=True, null=True)
    name_fn = models.CharField(verbose_name="نام انگلیسی",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    condition = models.CharField(verbose_name="وضعیت",max_length=100, unique=False, blank=True, null=True)
    area = models.FloatField(verbose_name="مساحت",unique=False, blank=True, null=True)
    build_ty = models.CharField(verbose_name="نوع ساختمان",max_length=100, unique=False, blank=True, null=True)
    ceiling_ty = models.CharField(verbose_name="نوع سقف",max_length=100, unique=False, blank=True, null=True)
    comment= models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "واحد"
        verbose_name_plural = "واحد"

class Cable_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام یا شماره",max_length=100, unique=False, blank=True, null=True)
    typ = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    voltage = models.FloatField(verbose_name="ولتاژ",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت",unique=False, blank=True, null=True)
    depth = models.FloatField(verbose_name="عمق کار",unique=False, blank=True, null=True)
    sze = models.FloatField(verbose_name="اندازه",unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False) 
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کابل"
        verbose_name_plural = "کابل"   

class Hydrator_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "هیدراتور"
        verbose_name_plural = "هیدراتور"

class Hydrator_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "هیدراتور"
        verbose_name_plural = "هیدراتور"

class Pilar_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پیلار"
        verbose_name_plural = "پیلار"

class Pilar_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پیلار"
        verbose_name_plural = "پیلار"

class Fire_Extingiuseher_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کپسول آتشنشانی"
        verbose_name_plural = "کپسول آتشنشانی"

class Fire_Extingiuseher_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کپسول آتشنشانی"
        verbose_name_plural = "کپسول آتشنشانی"

class Sump_pump_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سامپ پمپ"
        verbose_name_plural = "سامپ پمپ" 

class Fan_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فن"
        verbose_name_plural = "فن"

class Fan_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فن"
        verbose_name_plural = "فن"

class Unit_Pl(LinkedToLayerTable):
    name_en = models.CharField(verbose_name="نام فارسی",max_length=100, unique=False, blank=True, null=True)
    name_fn = models.CharField(verbose_name="نام انگلیسی",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    condition = models.CharField(verbose_name="وضعیت",max_length=100, unique=False, blank=True, null=True)
    area = models.FloatField(verbose_name="مساحت",unique=False, blank=True, null=True)
    build_ty = models.CharField(verbose_name="نوع ساختمان",max_length=100, unique=False, blank=True, null=True)
    ceiling_ty = models.CharField(verbose_name="نوع سقف",max_length=100, unique=False, blank=True, null=True)
    comment= models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "واحد"
        verbose_name_plural = "واحد"

class Unit_Pt(LinkedToLayerTable):
    name_en = models.CharField(verbose_name="نام فارسی",max_length=100, unique=False, blank=True, null=True)
    name_fn = models.CharField(verbose_name="نام انگلیسی",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="موقعیت",max_length=100, unique=False, blank=True, null=True)
    condition = models.CharField(verbose_name="وضعیت",max_length=100, unique=False, blank=True, null=True)
    area = models.FloatField(verbose_name="مساحت",unique=False, blank=True, null=True)
    build_ty = models.CharField(verbose_name="نوع ساختمان",max_length=100, unique=False, blank=True, null=True)
    ceiling_ty = models.CharField(verbose_name="نوع سقف",max_length=100, unique=False, blank=True, null=True)
    comment= models.CharField(verbose_name="توضیحات",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "واحد"
        verbose_name_plural = "واحد"

class Other_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سایر تجهیزات"
        verbose_name_plural = "سایر تجهیزات"

class Platform_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پلتفرم"
        verbose_name_plural = "پلتفرم"

class Platform_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پلتفرم"
        verbose_name_plural = "پلتفرم"

class Cooling_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیستم سرمایشی"
        verbose_name_plural = "سیستم سرمایشی"

class Cooling_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیستم سرمایشی"
        verbose_name_plural = "سیستم سرمایشی"

class Cooling_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیستم سرمایشی"
        verbose_name_plural = "سیستم سرمایشی"

class Heating_system_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیستم های گرمایشی"
        verbose_name_plural = "سیستم های گرمایشی"

class Power_Water_Gaz_Meter_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کنتور آب برق گاز"
        verbose_name_plural = "کنتور آب برق گاز"

class Power_Water_Gaz_Meter_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کنتور آب برق گاز"
        verbose_name_plural = "کنتور آب برق گاز"

class Warning_Sign_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "علائم هشداردهنده"
        verbose_name_plural = "علائم هشداردهنده"
        
class Warning_Sign_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "علائم هشداردهنده"
        verbose_name_plural = "علائم هشداردهنده"

class Sprinkler_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آبپاش"
        verbose_name_plural = "آبپاش" 

class Sprinkler_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "آبپاش"
        verbose_name_plural = "آبپاش" 


class Earthing_System_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیستم ارتینگ"
        verbose_name_plural = "سیستم ارتینگ"

class Earthing_System_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "سیستم ارتینگ"
        verbose_name_plural = "سیستم ارتینگ"

class Equipment_Box_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "جعبه تجهیزات"
        verbose_name_plural = "جعبه تجهیزات" 

class Equipment_Box_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "جعبه تجهیزات"
        verbose_name_plural = "جعبه تجهیزات"


class FlairـPt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فلایر"
        verbose_name_plural = "فلایر"

class FlairـPg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فلایر"
        verbose_name_plural = "فلایر"

class Aeration_BlowerـPt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "بلاورهای هوادهی"
        verbose_name_plural = "بلاورهای هوادهی"

class Aeration_BlowerـPg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "بلاورهای هوادهی"
        verbose_name_plural = "بلاورهای هوادهی"

class ChimenyـPt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دودکش"
        verbose_name_plural = "دودکش"

class ChimenyـPg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "دودکش"
        verbose_name_plural = "دودکش"

class Connector_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "اتصالات"
        verbose_name_plural = "اتصالات"
        
class Connector_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام دستگاه",max_length=100, unique=False, blank=True, null=True)
    application_ty = models.CharField(verbose_name="نوع کاربرد",max_length=100, unique=False, blank=True, null=True)
    code = models.CharField(verbose_name="کد دستگاه",max_length=100, unique=False, blank=True, null=True)
    serial_n = models.CharField(verbose_name="شماره سریال",max_length=100, unique=False, blank=True, null=True)
    location = models.CharField(verbose_name="محل استقرار",max_length=100, unique=False, blank=True, null=True)
    model = models.CharField(verbose_name="مدل دستگاه",max_length=100, unique=False, blank=True, null=True)
    manufacturing_country = models.CharField(verbose_name="کشور سازنده",max_length=100, unique=False, blank=True, null=True)
    year_construction = models.DateField(verbose_name="سال ساخت",auto_now=False,auto_now_add=False,null=True,blank=True)
    length = models.FloatField(verbose_name="طول",unique=False, blank=True, null=True)
    width = models.FloatField(verbose_name="عرض",unique=False, blank=True, null=True)
    height = models.FloatField(verbose_name="ارتفاع",unique=False, blank=True, null=True)
    weight = models.FloatField(verbose_name="وزن",unique=False, blank=True, null=True)
    power = models.FloatField(verbose_name="قدرت",unique=False, blank=True, null=True)
    engine_rpm = models.FloatField(verbose_name="دور موتور",unique=False, blank=True, null=True)
    capacity = models.FloatField(verbose_name="ظرفیت دستگاه",unique=False, blank=True, null=True)
    diameter = models.FloatField(verbose_name="قطر",unique=False, blank=True, null=True)
    material_density = models.FloatField(verbose_name="چگالی مواد",unique=False, blank=True, null=True)
    remaining_time = models.FloatField(verbose_name="زمان باقی مانده",unique=False, blank=True, null=True)
    volume = models.FloatField(verbose_name="حجم کاری",unique=False, blank=True, null=True)
    technical_specifications = models.CharField(verbose_name="مشخصات فنی",max_length=250, unique=False, blank=True, null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "اتصالات"
        verbose_name_plural = "اتصالات"