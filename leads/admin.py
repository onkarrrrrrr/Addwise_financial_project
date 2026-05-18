from django.contrib import admin
from .models import Appointment, CareerApplication, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'application_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'job_description')
    
    def application_count(self, obj):
        return obj.applications.count()
    application_count.short_description = 'Applications'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'service', 'created_at')
    list_filter = ('service', 'created_at')
    search_fields = ('full_name', 'email', 'phone')


@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'role', 'location', 'college', 'status', 'created_at')
    list_filter = ('status', 'role', 'created_at')
    search_fields = ('full_name', 'email', 'location', 'college', 'role__name')