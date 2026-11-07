from django.db import models
from django.db.models.expressions import RawSQL
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.indexes import GistIndex
from common.models.models import CustomModel

class Ostan(CustomModel):
    title = models.CharField(
        verbose_name="استان",
        max_length=128,
        unique=True,
        blank=False,
        null=False,
    )
    center = models.CharField(
        verbose_name="مرکز استان",
        max_length=128,
        unique=True,
        blank=False,
        null=True,
    )
    code = models.CharField(
        verbose_name="کد",
        max_length=5,
        unique=True,
        blank=False,
        null=False,
    )
    area_ha = models.FloatField(
        verbose_name="مساحت (هکتار)",
        null=True,
        blank=True,
        editable=False,
    )

    border = gis_models.MultiPolygonField(
        srid=3857,
        spatial_index=False,   # managed explicitly
        blank=False,
        null=False
    )
    @property
    def centroid(self):
        return [self.border.centroid.x , self.border.centroid.y]
    @property
    def bbox(self):
        return self.border.extent

    @property
    def area(self) -> float:
        "مساحت کل استان (هکتار)"
        return self.area_ha or 0.0
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # recompute in the database; update() doesn't call save(), so no recursion
        type(self).objects.filter(pk=self.pk).update(
            area_ha=RawSQL('ST_Area(ST_Transform(border, 4326)::geography) / 10000.0', [])
        )
        self.refresh_from_db(fields=['area_ha'])

    def __str__(self):
        return f"ostan {self.title} ({self.code})"
    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان ها"
        ordering = ["-created_at", "-id"]
        indexes = [
            GistIndex(fields=["border"], name="ostan_border_gist_idx"),
        ]

class Shahrestan(CustomModel):
    ostan = models.ForeignKey(
        Ostan,
        on_delete=models.CASCADE,
        related_name="shahrestans",
        blank=False,
        null=False,
    )
    title = models.CharField(
        verbose_name="نام",
        max_length=128,
        unique=False,
        blank=False,
        null=False,
    )
    code = models.CharField(
        verbose_name="کد",
        max_length=6,
        unique=True,
        blank=True,
        null=True,
    )
    border = gis_models.MultiPolygonField(
        srid=3857,
        spatial_index=False,   # managed explicitly
        blank=False,
        null=False
    )
    @property
    def centroid(self):
        return [self.border.centroid.x , self.border.centroid.y]
    @property
    def bbox(self):
        return self.border.extent

    def __str__(self):
        return f"Shahrestan {self.title}"
    class Meta:
        verbose_name = "شهرستان"
        verbose_name_plural = "شهرستان ها"
        ordering = ["-created_at", "-id"]
        indexes = [
            GistIndex(fields=["border"], name="shahrestan_border_gist_idx"),
        ]