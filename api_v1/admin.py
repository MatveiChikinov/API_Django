from django.contrib import admin
from .models import AgriculturalMachine, MaintenanceSchedule

@admin.register(AgriculturalMachine)
class AgriculturalMachineAdmin(admin.ModelAdmin):
    """Администрирование сельхозтехники."""
    list_display = ['id', 'name', 'model', 'machine_type', 'status', 'engine_hours', 'created_at']
    list_filter = ['machine_type', 'status', 'fuel_type']
    search_fields = ['name', 'model']

@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    """Администрирование графиков ТО."""
    list_display = ['id', 'machine', 'maintenance_type', 'priority', 'status', 'scheduled_date', 'cost']
    list_filter = ['maintenance_type', 'priority', 'status', 'scheduled_date']
    search_fields = ['machine__name', 'description']