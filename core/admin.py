from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter
from .models import CustomUser, Property

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin, UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('معلومات الحساب الإضافية', {
            'fields': ('full_name', 'phone_numbers', 'account_type', 'profile_picture', 'is_approved', 'rejection_notes')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('معلومات الحساب الإضافية', {
            'fields': ('full_name', 'phone_numbers', 'account_type', 'profile_picture', 'is_approved')
        }),
    )
    
    list_display = ('username', 'full_name', 'account_type', 'phone_numbers', 'is_approved', 'is_staff')
    list_filter = ('account_type', 'is_approved', 'is_staff')
    search_fields = ('username', 'full_name', 'phone_numbers', 'email')
    ordering = ('-date_joined',)
    
    actions = ['approve_selected_users', 'reject_selected_users']

    @admin.action(description="✅ اعتماد وتفعيل الحسابات المحددة")
    def approve_selected_users(self, request, queryset):
        rows_updated = queryset.update(is_approved=True, rejection_notes=None)
        self.message_user(request, f"تم بنجاح اعتماد وتفعيل {rows_updated} حساب/حسابات.")

    @admin.action(description="❌ رفض الحسابات المحددة")
    def reject_selected_users(self, request, queryset):
        rows_updated = queryset.update(is_approved=False, rejection_notes="تم الرفض من قبل الإدارة، يرجى التواصل لمعرفة السبب.")
        self.message_user(request, f"تم رفض {rows_updated} حساب/حسابات.")

@admin.register(Property)
class PropertyAdmin(ModelAdmin):
    list_display = ('title', 'price', 'owner', 'waiting_list', 'created_at')
    list_filter = ('waiting_list', 'created_at')
    search_fields = ('title', 'description', 'address', 'owner__full_name')
    date_hierarchy = 'created_at'
    
    actions = ['approve_selected_properties', 'reject_selected_properties']

    @admin.action(description="✅ اعتماد ونشر العقارات المحددة")
    def approve_selected_properties(self, request, queryset):
        rows_updated = queryset.update(waiting_list=False, rejection_notes=None)
        self.message_user(request, f"تم بنجاح اعتماد ونشر {rows_updated} عقار/عقارات.")

    @admin.action(description="❌ رفض العقارات المحددة")
    def reject_selected_properties(self, request, queryset):
        rows_updated = queryset.update(waiting_list=True, rejection_notes="تم رفض نشر الإعلان، يرجى مراجعة البيانات وإعادة الإرسال.")
        self.message_user(request, f"تم رفض {rows_updated} عقار/عقارات.")
