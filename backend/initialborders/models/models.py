from django.utils import timezone
from django.db.models import Q
from django.db import models , transaction
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models as gis_models
from common.models.models import CustomModel
from common.models.districts import Ostan
from contracts.models.models import Contract

def initial_dynamic_upload_path(instance, filename):
    return f'initialborder/erjaattachs/initialborder_{instance.rinitialborder.id}/{filename}'


class InitialBorderDomin(CustomModel):
    title = models.CharField(max_length=100, unique=True)
    code = models.IntegerField(unique=True)
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "نوع محدوده اولیه"
        verbose_name_plural = "انواع محدوده اولیه"

class InitialBorderMadeDomin(CustomModel):
    title = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "نوع ماده های محدوده اولیه"
        verbose_name_plural = "انواع ماده های محدوده اولیه"

class InitialBorder(CustomModel):
    title = models.CharField(
        max_length=250,
        unique=False,
        blank=False,
        null=False,
    )
    contracts = models.ManyToManyField(
        Contract,
        through="ContractInitialBorder",
        related_name="initborders",   # contract.initborders still works
        blank=True,
    )
    dtyp = models.ForeignKey(
        InitialBorderDomin,
        on_delete=models.SET_NULL,
        related_name="rinitialborderdomin",
        blank=True,
        null=True,
    )
    border = gis_models.MultiPolygonField(
        srid=3857,
        blank=False,
        null=False,
    )
    ostan = models.ManyToManyField(
        Ostan,
        verbose_name="استان",
        related_name="rostaninitialborder",
        blank=True,
    )

    code_cadaster = models.CharField(
        verbose_name="کد کاداستر",
        max_length=255,
        blank=True,
        null=True,
    )

    onvan_sazemani = models.CharField(
        verbose_name="عنوان سازمانی",
        max_length=255,
        blank=True,
        null=True,
    )

    code_sazemani = models.CharField(
        verbose_name="کد سازمانی",
        max_length=255,
        blank=True,
        null=True,
    )

    esm_mahali = models.CharField(
        verbose_name="اسم محلی",
        max_length=255,
        blank=True,
        null=True,
    )

    name_motaghazi = models.CharField(
        verbose_name="نام متقاظی",
        max_length=255,
        blank=True,
        null=True,
    )

    made = models.ManyToManyField(
        InitialBorderMadeDomin,
        verbose_name="نام ماده/گروه",
        blank=True,
        null=True,
        related_name='rinitmades',
    )

    file = models.FileField(
        verbose_name="فایل پیوست ارجاع محدوده",
        blank=False,
        upload_to=initial_dynamic_upload_path,
    )
    
    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
 
    @property
    def center(self):
        centroid = self.border.centroid
        return [centroid.x, centroid.y]
 
    @property
    def bbox(self):
        return self.border.extent
 
    def save(self, *args, **kwargs):
        # New instance, or existing one whose border geometry changed?
        border_changed = True
        if self.pk:
            old_border = (
                InitialBorder.objects.filter(pk=self.pk)
                .values_list("border", flat=True)
                .first()
            )
            if old_border is not None:
                border_changed = old_border != self.border
 
        with transaction.atomic():
            super().save(*args, **kwargs)
 
            if border_changed:
                intersecting = Ostan.objects.filter(
                    border__intersects=self.border
                )
                # set() replaces existing relations, so no need for clear()
                self.ostan.set(intersecting)
 
    def __str__(self):
        return self.title
 
    class Meta:
        verbose_name = "لیست محدوده اولیه"
        verbose_name_plural = "لیست محدوده‌های اولیه"

class ContractInitialBorder(CustomModel):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="border_links",
        verbose_name="قرارداد",
    )
    initial_border = models.ForeignKey(
        InitialBorder,
        on_delete=models.CASCADE,
        related_name="contract_links",
        verbose_name="محدوده اولیه",
    )

    class Meta:
        verbose_name = "ارتباط قرارداد و محدوده اولیه"
        verbose_name_plural = "ارتباط قراردادها و محدوده‌های اولیه"
        constraints = [
            models.UniqueConstraint(
                fields=["contract", "initial_border"],
                name="uniq_contract_initial_border",
            ),
        ]

    def _blocking_links(self):
        """Links of the same border whose contract is still active."""
        today = timezone.localdate()
        return (
            ContractInitialBorder.objects
            .filter(initial_border_id=self.initial_border_id)
            .exclude(pk=self.pk)
            .filter(contract__is_completed=False)
            .filter(
                Q(contract__end_date__isnull=True)
                | Q(contract__end_date__gte=today)
            )
        )

    def clean(self):
        super().clean()
        if not self.initial_border_id or not self.contract_id:
            return
        today = timezone.localdate()
        c = self.contract
        if c.is_completed or (c.end_date and c.end_date < today):
            return  # a finished contract can't conflict with an active one
        blocking = self._blocking_links().select_related("contract").first()
        if blocking:
            raise ValidationError(
                f"این محدوده اولیه هم‌اکنون به قرارداد «{blocking.contract.title}» "
                "متصل است. فقط پس از خاتمه یافتن آن (یا گذشتن تاریخ پایان) "
                "می‌توان آن را به قرارداد دیگری متصل کرد."
            )

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # lock the border row so two requests can't link it at the same time
            InitialBorder.objects.select_for_update().get(pk=self.initial_border_id)
            self.full_clean()
            super().save(*args, **kwargs)


#Attachment
from .attachment import *