from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet

from common.models import CustomModel
from common.models import Company

from initialborders.models.models import (
    InitialBorder
)

from contracts.models.models import (
    Contract,
    ContractBorder
)

from contracts.models.models import (
    ShrhLayer
)

class Apis(models.Model):
    # Define choices for HTTP methods
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH' , 'PATCH'),
        ('DELETE', 'DELETE'),
    ]
    # url_validator = RegexValidator(
    #     regex=r'^\/[a-zA-Z0-9_\-\/\{\}]*\/?$',
    #     message='فرمت URL نادرست است. باید با / شروع شود و فقط شامل حروف، اعداد، /، -، _ و {} باشد.'
    # )
    method = models.CharField(
        max_length=50, 
        choices=METHOD_CHOICES,
        blank=False, 
        null=False
    )
    url = models.CharField(
        max_length=250,
        # validators=[url_validator],
        blank=False,
        null= False
    )
    desc = models.CharField(
        max_length=250,
        blank=True,
        null= True
    )

    def __str__(self):
        return f"{self.method} _ {self.url}"
    class Meta:
        unique_together = ['method', 'url']
        indexes = [
            models.Index(fields=['method', 'url']),  # Composite index
            models.Index(fields=['url']),            # Individual indexes
            models.Index(fields=['method']),
        ]
        verbose_name = "نام دسترسی"
        verbose_name_plural = "لیست  دسترسی ها"

class Tools(models.Model):
    title = models.CharField(
        unique=True,
        max_length=100,
        blank=False,
        null=False
    )
    desc = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "ابزار دسترسی"
        verbose_name_plural = "ابزارهای دسترسی"

class Roles(models.Model):
    apis = models.ManyToManyField(
        Apis,
        blank=False,
        related_name='rrolesapis',
        related_query_name='rolesapis'
    )
    tools = models.ManyToManyField(
        Tools,
        blank=True,
        related_name='rroletools',
        related_query_name='roletools'
    )
    title = models.CharField(
        unique=True,
        max_length=100,
        blank=False,
        null=False
    )
    desc = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "نام نقش"
        verbose_name_plural = "لیست نقش ها"

class UserShrhLayerPermission(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    shrh_layer = models.ForeignKey(
        'contracts.ShrhLayer',
        on_delete=models.CASCADE,
        verbose_name="لایه شرح خدمات"
    )
    created_at = models.DateTimeField(
        verbose_name="تاریخ ایجاد",
        auto_now_add=True
    )
    
    class Meta:
        unique_together = ['user', 'shrh_layer']
        verbose_name = "دسترسی کاربر به لایه"
        verbose_name_plural = "دسترسی‌های کاربران به لایه‌ها"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['shrh_layer']),
            models.Index(fields=['user', 'shrh_layer']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.shrh_layer}"

class UserContractPermission(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    contract = models.ForeignKey(
        'contracts.Contract',
        on_delete=models.CASCADE,
        verbose_name="قرارداد"
    )
    
    class Meta:
        unique_together = ['user', 'contract']
        verbose_name = "دسترسی کاربر به قرارداد"
        verbose_name_plural = "دسترسی‌های کاربران به قراردادها"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['contract']),
            models.Index(fields=['user', 'contract']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.contract.title}"

class UserContractBorderPermission(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    contractborder = models.ForeignKey(
        'contracts.ContractBorder',
        on_delete=models.CASCADE,
        verbose_name="محدوده قرارداد"
    )
    
    class Meta:
        unique_together = ['user', 'contractborder']
        verbose_name = "دسترسی کاربر به محدوده قرارداد"
        verbose_name_plural = "دسترسی‌های کاربران به محدوده‌های قرارداد"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['contractborder']),
            models.Index(fields=['user', 'contractborder']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.contractborder.title}"

class UserInitialBorderPermission(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    initialborder = models.ForeignKey(
        'initialborders.InitialBorder',
        on_delete=models.CASCADE,
        verbose_name="محدوده اولیه"
    )
    
    class Meta:
        unique_together = ['user', 'initialborder']
        verbose_name = "دسترسی کاربر به محدوده اولیه"
        verbose_name_plural = "دسترسی‌های کاربران به محدوده‌های اولیه"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['initialborder']),
            models.Index(fields=['user', 'initialborder']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.initialborder.title}"

class User(AbstractUser):
    """
    Custom User model.
    """

    #Overwrite username field
    username_validator = RegexValidator(regex=r'^[0-9a-zA-Z]*$', message='فقط حروف و اعداد استفاده کنید')
    phone_validator = RegexValidator(regex=r'^989\d{9}$',message="شماره تماس باید با 989 شروع شود و دقیقاً 12 رقم باشد.")

    username = models.CharField(
      _("username"),
      max_length=25,
      unique=True,
      help_text=_(
          "اجباری.کمتر از 25 کاراکتر. فقط حروف و اعداد استفاده کنید"
      ),
      validators=[username_validator],
      error_messages={
          "unique": _("کاربر با این نام کاربری موجود است"),
      },
    )

    first_name_fa = models.CharField(verbose_name="نام فارسی", max_length=255, blank=True, null=True)
    last_name_fa = models.CharField(verbose_name="نام خانوادگی فارسی", max_length=255, blank=True, null=True)
    address = models.CharField(verbose_name="آدرس", max_length=255, blank=True, null=True)
    phonenumber = models.CharField(
        verbose_name="شماره تماس",
        max_length=255,
        blank=True,
        null=True,
        validators=[phone_validator]
    )
    codemeli = models.CharField(verbose_name="کد ملی", max_length=255, blank=True, null=True)
    fax = models.CharField(verbose_name="فکس", max_length=255, blank=True, null=True)

    start_access = models.DateField(verbose_name="تاریخ شروع دسترسی",auto_now=False,auto_now_add=False,null=True,blank=True)
    end_access = models.DateField(verbose_name="تاریخ پایان دسترسی",auto_now=False,auto_now_add=False,null=True,blank=True)

    user_attempt_login_limit = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False
    ) #check with setting.USER_TRY_LOGIN_LIMITAION

    roles = models.ForeignKey(
        Roles,
        on_delete=models.SET_NULL,
        related_name="rrole",
        blank=True,
        null=True,
        db_index=True  # Add index for faster lookups
    )

    is_controller = models.BooleanField(
        verbose_name="کنترل کننده است؟",
        default=False,
        blank=False,
        null=False,
        help_text="نشان می‌دهد که آیا این کاربر کنترل کننده پروژه است یا خیر",
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        related_name="rusercompany",
        blank=True,
        null=True,
        db_index=True  # Add index for faster lookups
    )
    
    # USER -> SharhLayer
    accessible_shrh_layers = models.ManyToManyField(
        'contracts.ShrhLayer',
        through='UserShrhLayerPermission',
        verbose_name="لایه‌های قابل دسترسی",
        blank=True,
        related_name="accessible_by_users"
    )
    # USER -> Contract
    accessible_contracts = models.ManyToManyField(
        'contracts.Contract',
        through='UserContractPermission',
        verbose_name="قراردادهای قابل دسترسی",
        blank=True,
        related_name="users_with_access_contracts",
        help_text="این فیلد به صورت خودکار بروزرسانی می‌شود"
    )
    # USER -> ContarctBorder
    accessible_contractborders = models.ManyToManyField(
        'contracts.ContractBorder',
        through='UserContractBorderPermission',
        verbose_name="محدوده‌های قرارداد قابل دسترسی",
        blank=True,
        related_name="users_with_access_contractborders",
        help_text="این فیلد به صورت خودکار بروزرسانی می‌شود"
    )
    # User -> InitialBorder
    accessible_initialborders = models.ManyToManyField(
        'initialborders.InitialBorder',
        through='UserInitialBorderPermission',
        verbose_name="محدوده‌های اولیه قابل دسترسی",
        blank=True,
        related_name="users_with_access_initialborders"
    )
    
    # ################## GET FROM USER ##################
    def get_accessible_contracts(self) -> QuerySet['Contract']:
        """
        Get all contracts this user has access to
        """
        return self.accessible_contracts.all()
    
    def get_accessible_contractborders(self) -> QuerySet['ContractBorder']:
        """
        Get all contract borders this user has access to
        """
        return self.accessible_contractborders.all()
    
    def get_accessible_initialborder(self) -> QuerySet['InitialBorder']:
        """
        Get all InitialBorders this user has access to
        """
        return self.accessible_initialborders.all()
    
    def get_accessible_contracts_with_details(self) -> QuerySet['Contract']:
        """
        Get accessible contracts with related data prefetched
        Use this when you need contract details
        """
        return self.accessible_contracts.select_related(
            'dtyp'
        ).prefetch_related(
            'shrh_items',
            'shrh_items__shr_layers',
            'initborder'
        )
    def get_accessible_shrhlayers_queryset(self) -> QuerySet:
        """
        Get QuerySet of all ShrhLayers this user has access to
        """
        return ShrhLayer.objects.filter(
            accessible_by_users=self
        )
    
    # ################## CHECK ACCESS ##################
    def has_contract_access(self, contract: Contract) -> bool:
        """
        Quick check if user has access to a specific contract
        """
        return UserContractPermission.objects.filter(
            user=self,
            contract=contract
        ).exists()
    
    def has_contractborder_access(self, contractborder: ContractBorder) -> bool:
        """
        Quick check if user has access to a specific ContractBorder
        """
        return UserContractBorderPermission.objects.filter(
            user=self,
            contractborder=contractborder
        ).exists()
    
    def has_access_to_initialborder(self, initial_border: InitialBorder) -> bool:
        """
        Check if the user has access to the given InitialBorder
        """
        return UserInitialBorderPermission.objects.filter(
            user=self,
            initialborder=initial_border
        ).exists()
    
    def has_sharhlayer_access(self, sharhlayer: ShrhLayer) -> bool:
        """
        Quick check if user has access to a specific ShrhLayer instance
        """
        return UserShrhLayerPermission.objects.filter(
            user=self,
            shrh_layer=sharhlayer
        ).exists()
    
    # ################## GRANT ONE INSTANCE ACCESS ##################
    def grant_contract_access(self, contract: Contract) -> bool:
        """
        Grant user access to a specific contract
        Returns True if access was granted, False if already had access
        """
        _, created = UserContractPermission.objects.get_or_create(
            user=self,
            contract=contract
        )
        return created

    def grant_contractborder_access(self, contractborder: ContractBorder) -> bool:
        """
        Grant user access to a specific contract border
        Returns True if access was granted, False if already had access
        """
        _, created = UserContractBorderPermission.objects.get_or_create(
            user=self,
            contractborder=contractborder
        )
        return created

    def grant_initialborder_access(self, initial_border: InitialBorder) -> bool:
        """
        Grant user access to a specific initial border
        Returns True if access was granted, False if already had access
        """
        _, created = UserInitialBorderPermission.objects.get_or_create(
            user=self,
            initialborder=initial_border
        )
        return created

    def grant_sharhlayer_access(self, sharhlayer: ShrhLayer) -> bool:
        """
        Grant user access to a specific ShrhLayer
        Returns True if access was granted, False if already had access
        """
        _, created = UserShrhLayerPermission.objects.get_or_create(
            user=self,
            shrh_layer=sharhlayer
        )
        return created

    # ################## REVOKE ONE INSTANCE ACCESS ##################
    def revoke_contract_access(self, contract: Contract) -> bool:
        """
        Revoke user access to a specific contract
        Returns True if access was revoked, False if didn't have access
        """
        deleted_count, _ = UserContractPermission.objects.filter(
            user=self,
            contract=contract
        ).delete()
        return deleted_count > 0

    def revoke_contractborder_access(self, contractborder: ContractBorder) -> bool:
        """
        Revoke user access to a specific contract border
        Returns True if access was revoked, False if didn't have access
        """
        deleted_count, _ = UserContractBorderPermission.objects.filter(
            user=self,
            contractborder=contractborder
        ).delete()
        return deleted_count > 0

    def revoke_initialborder_access(self, initial_border: InitialBorder) -> bool:
        """
        Revoke user access to a specific initial border
        Returns True if access was revoked, False if didn't have access
        """
        deleted_count, _ = UserInitialBorderPermission.objects.filter(
            user=self,
            initialborder=initial_border
        ).delete()
        return deleted_count > 0

    def revoke_sharhlayer_access(self, sharhlayer: ShrhLayer) -> bool:
        """
        Revoke user access to a specific ShrhLayer
        Returns True if access was revoked, False if didn't have access
        """
        deleted_count, _ = UserShrhLayerPermission.objects.filter(
            user=self,
            shrh_layer=sharhlayer
        ).delete()
        return deleted_count > 0

    # ################## GRANT BULK ACCESS ##################
    def grant_bulk_contract_access(self, contracts: list[Contract]) -> int:
        """
        Grant access to multiple contracts at once
        Returns count of newly granted accesses
        """
        existing_contract_ids = set(
            UserContractPermission.objects.filter(user=self).values_list('contract_id', flat=True)
        )
        new_permissions = [
            UserContractPermission(user=self, contract=contract)
            for contract in contracts
            if contract.id not in existing_contract_ids
        ]
        if new_permissions:
            UserContractPermission.objects.bulk_create(new_permissions, ignore_conflicts=True)
        return len(new_permissions)

    def grant_bulk_contractborder_access(self, contractborders: list[ContractBorder]) -> int:
        """
        Grant access to multiple contract borders at once
        Returns count of newly granted accesses
        """
        existing_border_ids = set(
            UserContractBorderPermission.objects.filter(user=self).values_list('contractborder_id', flat=True)
        )
        new_permissions = [
            UserContractBorderPermission(user=self, contractborder=cb)
            for cb in contractborders
            if cb.id not in existing_border_ids
        ]
        if new_permissions:
            UserContractBorderPermission.objects.bulk_create(new_permissions, ignore_conflicts=True)
        return len(new_permissions)

    def grant_bulk_initialborder_access(self, initialborders: list[InitialBorder]) -> int:
        """
        Grant access to multiple initial borders at once
        Returns count of newly granted accesses
        """
        existing_border_ids = set(
            UserInitialBorderPermission.objects.filter(user=self).values_list('initialborder_id', flat=True)
        )
        new_permissions = [
            UserInitialBorderPermission(user=self, initialborder=ib)
            for ib in initialborders
            if ib.id not in existing_border_ids
        ]
        if new_permissions:
            UserInitialBorderPermission.objects.bulk_create(new_permissions, ignore_conflicts=True)
        return len(new_permissions)
    
    def grant_bulk_sharhlayer_access(self, sharhlayers: list[ShrhLayer]) -> int:
        """
        Grant access to multiple ShrhLayers at once
        Returns count of newly granted accesses
        """
        existing_layer_ids = set(
            UserShrhLayerPermission.objects.filter(user=self).values_list('shrh_layer_id', flat=True)
        )
        new_permissions = [
            UserShrhLayerPermission(user=self, shrh_layer=layer)
            for layer in sharhlayers
            if layer.id not in existing_layer_ids
        ]
        if new_permissions:
            UserShrhLayerPermission.objects.bulk_create(new_permissions, ignore_conflicts=True)
        return len(new_permissions)
    
    # ################## REVOKE ALL ACCESS ##################
    def revoke_all_contract_access(self) -> int:
        """
        Revoke all contract accesses for this user
        Returns count of revoked accesses
        """
        deleted_count, _ = UserContractPermission.objects.filter(user=self).delete()
        return deleted_count

    def revoke_all_contractborder_access(self) -> int:
        """
        Revoke all contract border accesses for this user
        Returns count of revoked accesses
        """
        deleted_count, _ = UserContractBorderPermission.objects.filter(user=self).delete()
        return deleted_count

    def revoke_all_initialborder_access(self) -> int:
        """
        Revoke all initial border accesses for this user
        Returns count of revoked accesses
        """
        deleted_count, _ = UserInitialBorderPermission.objects.filter(user=self).delete()
        return deleted_count

    def revoke_all_sharhlayer_access(self) -> int:
        """
        Revoke all ShrhLayer accesses for this user
        Returns count of revoked accesses
        """
        deleted_count, _ = UserShrhLayerPermission.objects.filter(user=self).delete()
        return deleted_count

    def get_full_name_fa(self):
        full_name_fa = "%s %s" % (self.first_name_fa, self.last_name_fa)
        return full_name_fa.strip()

    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "نام کاربران"
        verbose_name_plural = "لیست کاربران"

class Notification(CustomModel):
    sender = models.ForeignKey(
        User,
        verbose_name="فرستنده",
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        blank=True, # Allow null for system notifications
        null=True, # Allow null for system notifications
        db_index=True,
    )
    receiver = models.ForeignKey(
        User,
        verbose_name="گیرنده",
        on_delete=models.CASCADE,
        related_name='received_notifications',
        blank=False,
        null=False,
        db_index=True
    )
    subject = models.CharField(
        verbose_name="موضوع" ,
        max_length=500,
        blank=False,
        null=False,
        unique=False,
    )
    text = models.CharField(
        verbose_name="متن" ,
        max_length=2000,
        blank=False,
        null=False,
        unique=False
    )
    is_read = models.BooleanField(
        verbose_name="وضعیت خوانده شده",
        default=False,
        blank=False,
        null=False
    )

    def __str__(self):
        sender_name = self.sender.username if self.sender else "سیستم"
        return f"اعلان: از {sender_name} به {self.receiver.username} - {self.subject[:30]}..."
    
    class Meta:
        verbose_name = "اعلان"
        verbose_name_plural = "اعلان ها"
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=['receiver', '-created_at']),
            models.Index(fields=['sender', '-created_at']),
        ]