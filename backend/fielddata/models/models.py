# import os
# from django.db import models

# from django.core.exceptions import ValidationError

# from common.models import CustomModel
# from accounts.models import User
# from contracts.models.models import (
#     Contract,
#     ContractDomin
# )


# class ContractStep(CustomModel):
#     """
#         Exp: "شناسایی" , "پیجویی" , ""
#     """
#     dtyp = models.ForeignKey(
#         ContractDomin,
#         verbose_name="نوع قرارداد",
#         on_delete=models.SET_NULL,
#         related_name="rdtypcontractsteps",
#         blank=True, 
#         null=True,
#     )
#     title = models.CharField(
#         verbose_name="عنوان",
#         max_length=250,
#         blank=False,
#         null=False,
#     )
#     def __str__(self):
#         return f"مرحله قرارداد  {self.title} --- ({self.dtyp.title})"

#     class Meta:
#         verbose_name = "مراحه قرارداد"
#         verbose_name_plural = "مراحل قرارداد"

# class GeochemistaryFieldData(CustomModel):
#     """
#         - برگه کوچیکه

#     """
#     SAMPLETYPE_CHOICES = [
#         ("rock" , "ROCK"),
#         ("soil" , "SOIL"),
#         ("stream" , "STREAM"),
#     ]

#     dstep = models.ForeignKey(
#         ContractStep,
#         verbose_name="مرحله قرارداد",
#         on_delete=models.SET_NULL,
#         related_name="rstepfielddatageochemistary",
#         blank=True, 
#         null=True,
#     )

#     contract = models.ForeignKey(
#         Contract,
#         verbose_name="قرارداد مربوطه",
#         on_delete=models.CASCADE,
#         # related_name="rcontractfielddatageochemistary",
#         blank=False, 
#         null=False,
#     )

#     user = models.ForeignKey(
#         User,
#         verbose_name="کاربر نویسنده",
#         on_delete=models.CASCADE,
#         # related_name="ruserfielddatageochemistary",
#         blank=False, 
#         null=False,
#     )

#     sample_type = models.CharField(
#         choices=SAMPLETYPE_CHOICES,
#         max_length=100,
#         unique=False,
#         blank=False,
#         null=False,
#         error_messages={
#             'invalid_choice': f'انتخاب نامعتبر است. گزینه‌های معتبر: {", ".join([f"{choice[0]} ({choice[1]})" for choice in SAMPLETYPE_CHOICES])}'
#         }
#     )

#     sample_code = models.CharField(max_length=250 , blank=True , null=True)
#     sample_no = models.CharField(max_length=250 , blank=True , null=True)

#     coordinate = models.CharField(max_length=250 , blank=True , null=True)
#     zone = models.CharField(max_length=250 , blank=True , null=True)
#     x =  models.CharField(max_length=250 , blank=True , null=True)
#     y = models.CharField(max_length=250 , blank=True , null=True)
#     z = models.CharField(max_length=250 , blank=True , null=True)
    
#     mineralization_alteration = models.CharField(max_length=500 , blank=True , null=True)

#     #structure type
#     strike = models.CharField(max_length=250 , blank=True , null=True)
#     dip = models.CharField(max_length=250 , blank=True , null=True)
#     dip_direction = models.CharField(max_length=250 , blank=True , null=True)
#     thickness_m = models.FloatField(blank=True , null=True)
#     length_m = models.FloatField(blank=True , null=True)
#     geometry = models.CharField(max_length=250 , blank=True , null=True)
#     density = models.CharField(max_length=250 , blank=True , null=True)

#     #drilling 
#     interval = models.CharField(max_length=250 , blank=True , null=True)
#     drilling_frm= models.CharField(max_length=250 , blank=True , null=True)
#     drilling_to = models.CharField(max_length=250 , blank=True , null=True)

#     photo_no_frm = models.CharField(max_length=250 , blank=True , null=True)
#     photo_no_to = models.CharField(max_length=250 , blank=True , null=True)

#     class Meta:
#         abstract = True


# class GeochemistaryFieldDataRock(GeochemistaryFieldData):
#     #rock unit description
#     lithology = models.CharField(max_length=250 , blank=True , null=True)
#     channel_no  = models.CharField(max_length=250 , blank=True , null=True)
#     sample_no_in_channel = models.CharField(max_length=250 , blank=True , null=True)
#     trend  = models.CharField(max_length=250 , blank=True , null=True)
#     frm  = models.CharField(max_length=250 , blank=True , null=True)
#     to  = models.CharField(max_length=250 , blank=True , null=True)

#     def clean(self):
#         if self.sample_type != "rock":
#             raise ValidationError("این جدول فقط برای نمونه های rock قابل استفاده است")
#         super().clean()
        
#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f" گزارش صحرایی  ژیوشیمی (rock) قرارداد  {self.contract.title}"

#     class Meta:
#         verbose_name = "گزارش صحرایی ژیوشیمی (rock)"
#         verbose_name_plural = " گزارش های صحرایی ژیوشیمی (rock)"


# class GeochemistaryFieldDataSoil(GeochemistaryFieldData):
#     #solid sample desctiption 
#     typ = models.CharField(max_length=250 , blank=True , null=True)
#     horizon = models.CharField(max_length=250 , blank=True , null=True)
#     color = models.CharField(max_length=250 , blank=True , null=True)
#     slope = models.CharField(max_length=250 , blank=True , null=True)
#     land_use = models.CharField(max_length=250 , blank=True , null=True)
#     clay = models.CharField(max_length=250 , blank=True , null=True)
#     silt_percent = models.FloatField(blank=True , null=True)
#     sand_percent = models.FloatField(blank=True , null=True)
#     gravel_percent = models.FloatField(blank=True , null=True)
#     organic_matter_percent = models.FloatField(blank=True , null=True)

#     def clean(self):
#         if self.sample_type != "soil":
#             raise ValidationError("این جدول فقط برای نمونه های soil قابل استفاده است")
#         super().clean()
        
#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f" گزارش صحرایی  ژیوشیمی (soil) قرارداد  {self.contract.title}"

#     class Meta:
#         verbose_name = "گزارش صحرایی ژیوشیمی (soil)"
#         verbose_name_plural = " گزارش های صحرایی ژیوشیمی (soil)"


# class GeochemistaryFieldDataStream(GeochemistaryFieldData):
#     steram = models.CharField(max_length=250 , blank=True , null=True)
#     steram_color  = models.CharField(max_length=250 , blank=True , null=True)
#     steram_sieve  = models.CharField(max_length=250 , blank=True , null=True)
#     wet_dry  = models.CharField(max_length=250 , blank=True , null=True)
#     contamination = models.CharField(max_length=250 , blank=True , null=True)


#     def clean(self):
#         if self.sample_type != "stream":
#             raise ValidationError("این جدول فقط برای نمونه های stream قابل استفاده است")
#         super().clean()
        
#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f" گزارش صحرایی  ژیوشیمی (rock) قرارداد  {self.contract.title}"

#     class Meta:
#         verbose_name = "گزارش صحرایی ژیوشیمی (rock)"
#         verbose_name_plural = " گزارش های صحرایی ژیوشیمی (rock)"












