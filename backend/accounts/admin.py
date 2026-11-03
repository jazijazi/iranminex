from django.contrib import admin
from django_admin_inline_paginator.admin import TabularInlinePaginated
from django.contrib.auth.admin import UserAdmin
from accounts.models import (
    User,
    Apis,
    Tools,
    Roles,
    Notification,
)
from .models import UserShrhLayerPermission , UserContractPermission , UserContractBorderPermission , UserInitialBorderPermission
from accounts.forms import UserAdminForm
from django.utils.html import format_html
from django import forms
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

class SendNotificationForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    subject = forms.CharField(
        label="موضوع پیام", 
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
    )
    text = forms.CharField(
        label="متن پیام", 
        widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 5, 'style': 'width: 100%;'})
    )
class APISADMIN(admin.ModelAdmin):
    list_display = ['id', 'method', 'url', 'desc']
    list_filter = ['method']
    search_fields = ['method', 'url', 'desc']
    ordering = ['method', 'url']
    list_per_page = 50
    
    fieldsets = (
        ('API تنظیمات', {
            'fields': ('method', 'url', 'desc'),
            'description': format_html(
                '<div style="direction: rtl;padding: 15px; border-left: 6px solid #2196F3; margin-bottom: 20px;">'
                '<strong style="color:red;font-size:1.6rem;">راهنمای استفاده:</strong><br>'
                '• برای URLهای با پارامتر دینامیک از <code>{{id}}</code> استفاده کنید<br>'
                '• مثال: <code>/api/initialborders/{{id}}/attachments/</code><br>'
                '• مثال: <code>/api/users/{{id}}/</code><br>'
                '• URL باید با <code>/</code> شروع شود<br>'
                '• کاراکترهای مجاز: حروف، اعداد، <code>/</code>، <code>-</code>، <code>_</code>، <code>{{}}</code>'
                '</div>'
            )
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['url'].help_text = (
            'برای پارامترهای دینامیک از {id} استفاده کنید. '
            'مثال: /api/initialborders/{id}/attachments/'
        )
        form.base_fields['method'].help_text = 'نوع درخواست HTTP را انتخاب کنید'
        form.base_fields['desc'].help_text = 'توضیحات اختیاری درباره این API'
        return form
    class Meta:
        verbose_name = 'API'
        verbose_name_plural = 'APIs'
class TOOLSADMIN(admin.ModelAdmin):
    list_display = ['id' , 'title']
    search_fields = ['title']

class ROLESADMIN(admin.ModelAdmin):
    list_display = ['id' , 'title']
    search_fields = ['title']
    filter_horizontal = ['apis', 'tools']

# ################## INLINE ADMIN CLASSES ##################
class UserShrhLayerPermissionInline(TabularInlinePaginated):
    model = UserShrhLayerPermission
    extra = 2
    verbose_name = "دسترسی به لایه شرح خدمات"
    verbose_name_plural = "دسترسی‌های لایه شرح خدمات"
    autocomplete_fields = ['shrh_layer']
    fields = ['shrh_layer']
    classes = ['collapse']
    per_page = 30


class UserContractPermissionInline(TabularInlinePaginated):
    model = UserContractPermission
    extra = 2
    verbose_name = "دسترسی به قرارداد"
    verbose_name_plural = "دسترسی‌های قرارداد"
    autocomplete_fields = ['contract']
    fields = ['contract']
    classes = ['collapse']
    per_page = 15


class UserContractBorderPermissionInline(TabularInlinePaginated):
    model = UserContractBorderPermission
    extra = 2
    verbose_name = "دسترسی به محدوده قرارداد"
    verbose_name_plural = "دسترسی‌های محدوده قرارداد"
    autocomplete_fields = ['contractborder']
    fields = ['contractborder']
    classes = ['collapse']
    per_page = 15


class UserInitialBorderPermissionInline(TabularInlinePaginated):
    model = UserInitialBorderPermission
    extra = 2
    verbose_name = "دسترسی به محدوده اولیه"
    verbose_name_plural = "دسترسی‌های محدوده اولیه"
    autocomplete_fields = ['initialborder']
    fields = ['initialborder']
    classes = ['collapse']
    per_page = 15

class USERSINADMIN(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['id','username','first_name_fa','last_name_fa','roles','company__name','is_active','is_superuser']
    list_filter = ['is_active', 'is_superuser']
    search_fields = ['username','first_name_fa','last_name_fa','first_name','last_name']
    list_display_links = ['username']
    # Add autocomplete fields here
    inlines = [
        UserInitialBorderPermissionInline,
        UserContractPermissionInline,
        UserContractBorderPermissionInline,
        UserShrhLayerPermissionInline,
    ]
    fieldsets = (
        ('اطلاعات کاربری', {
            'fields': ('username',
                       'password',
                       'first_name', 'last_name',
                       'first_name_fa', 'last_name_fa', 'email',
                       'address',
                    ),
        }),
        ('وضعیت و نقش', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_controller', 'roles', 'company','user_attempt_login_limit'),
            'classes': ('collapse',)
        }),
        ('تاریخ‌ها', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
        ('سایر اطلاعات', {
            'fields': ('phonenumber','codemeli','fax','start_access','end_access'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']


    actions = ['send_custom_notification_action']

    def send_custom_notification_action(self, request, queryset):
        # 1. If the form is submitted (POST) and contains the 'apply' button
        if 'apply' in request.POST:
            form = SendNotificationForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                text = form.cleaned_data['text']
                
                count = 0
                # Create notifications for selected users
                notifications_to_create = []
                for user in queryset:
                    notifications_to_create.append(
                        Notification(
                            sender=request.user, # The Admin user sending the message
                            receiver=user,
                            subject=subject,
                            text=text
                        )
                    )
                    count += 1
                
                # Bulk create for performance
                Notification.objects.bulk_create(notifications_to_create)
                
                # Show success message
                self.message_user(request, f"پیام با موفقیت برای {count} کاربر ارسال شد.", messages.SUCCESS)
                
                # Return to the user list
                return HttpResponseRedirect(request.get_full_path())
                
        # 2. If this is the first time clicking the action (Initial GET/POST)
        else:
            # Prepare the form with the selected users
            initial_data = {
                '_selected_action': request.POST.getlist(ACTION_CHECKBOX_NAME),
            }
            form = SendNotificationForm(initial=initial_data)

        # 3. Render the Intermediate Page
        return render(
            request,
            'admin/send_notification_intermediate.html',
            context={
                'users': queryset,
                'form': form,
                'title': 'ارسال اعلان دستی',
                'opts': self.model._meta,
                'action_checkbox_name': ACTION_CHECKBOX_NAME,
            }
        )

    send_custom_notification_action.short_description = "ارسال اعلان (Notification) به کاربران انتخاب شده"
    
    #readonly_fields = []    
    #actions = []
    
class NotificationAmin(admin.ModelAdmin):
    list_display = ['id' , 'sender' , 'receiver' , 'created_at']
    list_display_links = ['id' , 'sender' , 'receiver' ]
    list_per_page = 200

admin.site.register(User, USERSINADMIN)
admin.site.register(Apis , APISADMIN)
admin.site.register(Tools , TOOLSADMIN)
admin.site.register(Roles , ROLESADMIN)
admin.site.register(Notification, NotificationAmin)