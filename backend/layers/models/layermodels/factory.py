from django.db import models
from django.contrib.gis.db import models as gis_models

from layers.models.models import LinkedToLayerTable


class Factory_Pelan_Pg(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام" ,max_length=250, unique=False,blank=True,null=True)
    border = gis_models.MultiPolygonField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پلان"
        verbose_name_plural = "پلان"

class Factory_Pelan_Pl(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام" ,max_length=250, unique=False,blank=True,null=True)
    border = gis_models.MultiLineStringField(srid=4326, blank=False, null=False) 

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پلان"
        verbose_name_plural = "پلان"

class Factory_Pelan_Pt(LinkedToLayerTable):
    name = models.CharField(verbose_name="نام" ,max_length=250, unique=False,blank=True,null=True)
    border = gis_models.MultiPointField(srid=4326, blank=False, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "پلان"
        verbose_name_plural = "پلان"
