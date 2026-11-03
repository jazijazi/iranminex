# from django.contrib.gis.db import models as gis_models
# from django.db import models
# from django.core.exceptions import ValidationError
# from common.models import CustomModel
# from accounts.models import User
# from contracts.models.models import (
#     Contract,
#     ContractDomin
# )


# class GeochemSample(CustomModel):

#     contract = models.ForeignKey(
#         "Contract",
#         on_delete=models.CASCADE,
#         related_name="%(class)s_samples",
#     )

#     dstep = models.ForeignKey(
#         "ContractStep",
#         on_delete=models.CASCADE,
#         related_name="%(class)s_dstep",
#     )

#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="%(class)s_user",
#     )

#     sample_code = models.CharField(max_length=100, db_index=True)
#     sample_no = models.CharField(max_length=100, blank=True, null=True)

#     zone = models.CharField(max_length=200, blank=True, null=True)
#     x =  models.CharField(max_length=250 , blank=True , null=True)
#     y = models.CharField(max_length=250 , blank=True , null=True)
#     z = models.CharField(max_length=250 , blank=True , null=True)

#     photo_from = models.CharField(max_length=100, blank=True, null=True)
#     photo_to = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         pass

#     def __str__(self):
#         return f"{self.sample_code} - {self.contract}"


# class Structure(models.Model):

#     sample = models.ForeignKey(
#         GeochemSample,
#         on_delete=models.CASCADE,
#         related_name="structures",
#     )

#     strike = models.FloatField(null=True, blank=True)
#     dip = models.FloatField(null=True, blank=True)
#     dip_direction = models.FloatField(null=True, blank=True)

#     thickness_m = models.FloatField(null=True, blank=True)
#     length_m = models.FloatField(null=True, blank=True)

#     geometry = models.CharField(max_length=200, blank=True, null=True)
#     density = models.FloatField(null=True, blank=True)

#     def __str__(self):
#         return f"Structure - {self.sample.sample_code}"


# class ChannelSegment(models.Model):

#     sample = models.OneToOneField(
#         GeochemSample,
#         on_delete=models.CASCADE,
#         related_name="channel_segment",
#     )

#     channel_no = models.CharField(max_length=100)
#     trend = models.FloatField(null=True, blank=True)

#     from_m = models.FloatField()
#     to_m = models.FloatField()

#     def clean(self):
#         if self.to_m <= self.from_m:
#             raise ValidationError("to_m must be greater than from_m")

#     def __str__(self):
#         return f"Channel {self.channel_no} - {self.sample.sample_code}"

# class DrillInterval(models.Model):

#     sample = models.OneToOneField(
#         GeochemSample,
#         on_delete=models.CASCADE,
#         related_name="drill_interval",
#     )

#     from_m = models.FloatField()
#     to_m = models.FloatField()

#     def clean(self):
#         if self.to_m <= self.from_m:
#             raise ValidationError("to_m must be greater than from_m")

#     def __str__(self):
#         return f"Drill - {self.sample.sample_code}"


# class RockSample(models.Model):

#     sample = models.OneToOneField(
#         GeochemSample,
#         on_delete=models.CASCADE,
#         related_name="rock",
#     )

#     lithology = models.CharField(max_length=200, blank=True, null=True)
#     mineralization_alteration = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"Rock - {self.sample.sample_code}"

# class SoilSample(models.Model):

#     sample = models.OneToOneField(
#         GeochemSample,
#         on_delete=models.CASCADE,
#         related_name="soil",
#     )

#     horizon = models.CharField(max_length=100, blank=True, null=True)
#     color = models.CharField(max_length=100, blank=True, null=True)
#     slope = models.CharField(max_length=100, blank=True, null=True)
#     land_use = models.CharField(max_length=200, blank=True, null=True)

#     clay_percent = models.FloatField(null=True, blank=True)
#     silt_percent = models.FloatField(null=True, blank=True)
#     sand_percent = models.FloatField(null=True, blank=True)
#     gravel_percent = models.FloatField(null=True, blank=True)
#     organic_matter_percent = models.FloatField(null=True, blank=True)

#     def __str__(self):
#         return f"Soil - {self.sample.sample_code}"

# class StreamSample(models.Model):

#     sample = models.OneToOneField(
#         GeochemSample,
#         on_delete=models.CASCADE,
#         related_name="stream",
#     )

#     stream_name = models.CharField(max_length=200, blank=True, null=True)
#     color = models.CharField(max_length=100, blank=True, null=True)
#     sieve = models.CharField(max_length=100, blank=True, null=True)
#     wet_dry = models.CharField(max_length=50, blank=True, null=True)
#     contamination = models.CharField(max_length=200, blank=True, null=True)

#     def __str__(self):
#         return f"Stream - {self.sample.sample_code}"
