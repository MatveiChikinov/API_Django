from django.db import models

class AgriculturalMachine(models.Model):
    """Модель сельхозтехники"""
    TYPE_CHOICES = [
        ('tractor', 'Трактор'),
        ('harvester', 'Комбайн'),
        ('plow', 'Плуг'),
        ('seeder', 'Сеялка'),
    ]
    STATUS_CHOICES = [
        ('active', 'В работе'),
        ('maintenance', 'На ТО'),
        ('repair', 'В ремонте'),
        ('inactive', 'Неактивна'),
    ]

    name = models.CharField(max_length=150, verbose_name="Название")
    model = models.CharField(max_length=100, verbose_name="Модель")
    machine_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    fuel_type = models.CharField(max_length=50, verbose_name="Тип топлива")
    engine_hours = models.FloatField(default=0.0, verbose_name="Моточасы")
    manufacture_year = models.IntegerField(null=True, blank=True, verbose_name="Год выпуска")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.name} ({self.model})"


class MaintenanceSchedule(models.Model):
    """График технического обслуживания"""
    MAINTENANCE_TYPES = [
        ('routine', 'Плановое ТО'),
        ('repair', 'Ремонт'),
        ('inspection', 'Инспекция'),
        ('seasonal', 'Сезонное обслуживание'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    STATUS_TO_CHOICES = [
        ('scheduled', 'Запланировано'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
    ]

    machine = models.ForeignKey(AgriculturalMachine, on_delete=models.CASCADE, related_name='maintenances',verbose_name="Техника")
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES, verbose_name="Тип работ")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Приоритет")
    status = models.CharField(max_length=20, choices=STATUS_TO_CHOICES, default='scheduled', verbose_name="Статус")
    scheduled_date = models.DateField(verbose_name="Дата ТО")
    description = models.TextField(blank=True, verbose_name="Описание")
    cost = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Стоимость")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ТО для {self.machine.name} - {self.scheduled_date}"