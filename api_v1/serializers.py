from rest_framework import serializers
from .models import AgriculturalMachine, MaintenanceSchedule

class AgriculturalMachineSerializer(serializers.ModelSerializer):
    """Сериализатор для модели AgriculturalMachine.
    При чтении отдаёт список ID связанных графиков ТО.
    Поля id и created_at доступны только для чтения.
    """
    maintenances = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = AgriculturalMachine
        fields = [
            'id', 'name', 'model', 'machine_type', 'status', 'fuel_type',
            'engine_hours', 'manufacture_year', 'maintenances', 'created_at'
        ]


class MaintenanceScheduleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели MaintenanceSchedule.
    При чтении отдаёт строковое представление техники.
    При создании принимает только ID техники в поле machine_id.
    """
    machine = serializers.StringRelatedField(read_only=True)
    machine_id = serializers.PrimaryKeyRelatedField(
        queryset=AgriculturalMachine.objects.all(),
        source='machine',
        write_only=True
    )

    class Meta:
        model = MaintenanceSchedule
        fields = [
            'id', 'machine', 'machine_id', 'maintenance_type', 'priority',
            'status', 'scheduled_date', 'description', 'cost', 'created_at'
        ]