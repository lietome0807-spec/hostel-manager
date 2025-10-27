from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Room, Bed, Resident, SystemSettings, AuditLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'status', 'is_super_admin', 'access_until', 'created_at']
    list_filter = ['status', 'is_super_admin', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('status', 'access_until', 'is_super_admin')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('status', 'access_until', 'is_super_admin')
        }),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_total_beds', 'get_free_beds', 'get_occupied_beds', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ['room', 'bed_number', 'bed_type', 'side', 'is_occupied', 'position']
    list_filter = ['bed_type', 'side', 'is_occupied', 'room']
    search_fields = ['room__name', 'bed_number']
    ordering = ['room', 'position']


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ['name', 'room', 'bed_number', 'check_in_date', 'check_out_date', 'payment_status', 'payment_amount']
    list_filter = ['payment_status', 'room', 'check_in_date', 'check_out_date']
    search_fields = ['name', 'passport_number', 'phone_number']
    ordering = ['-created_at']
    date_hierarchy = 'check_in_date'


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'updated_at']
    search_fields = ['key', 'value', 'description']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'details', 'ip_address']
    ordering = ['-timestamp']
    readonly_fields = ['user', 'action', 'details', 'ip_address', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
