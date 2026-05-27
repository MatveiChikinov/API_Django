from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

from .models import AgriculturalMachine, MaintenanceSchedule
from .serializers import AgriculturalMachineSerializer, MaintenanceScheduleSerializer


class AgriculturalMachineViewSet(viewsets.ModelViewSet):
    """Представление для работы с сельхозтехникой.
    Поддерживает все CRUD-операции, включая массовое создание,
    обновление и удаление. GET-запросы кешируются на 15 минут.
    Фильтрация: name, machine_type, status, min_engine_hours, max_engine_hours.
    """
    serializer_class = AgriculturalMachineSerializer
    queryset = AgriculturalMachine.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        machine_type = self.request.query_params.get('machine_type')
        status_param = self.request.query_params.get('status')
        min_hours = self.request.query_params.get('min_engine_hours')
        max_hours = self.request.query_params.get('max_engine_hours')

        if name:
            qs = qs.filter(name__icontains=name)
        if machine_type:
            qs = qs.filter(machine_type=machine_type)
        if status_param:
            qs = qs.filter(status=status_param)
        if min_hours:
            qs = qs.filter(engine_hours__gte=float(min_hours))
        if max_hours:
            qs = qs.filter(engine_hours__lte=float(max_hours))
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одной или нескольких единиц техники."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-обновление одной или нескольких единиц техники."""
        many = isinstance(request.data, list)
        if many:
            instances = [AgriculturalMachine.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одной или нескольких единиц техники."""
        many = isinstance(request.data, list)
        if many:
            instances = [AgriculturalMachine.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одной или нескольких единиц техники (?ids=1,2,3)."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            AgriculturalMachine.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class MaintenanceScheduleViewSet(viewsets.ModelViewSet):
    """Представление для работы с графиками ТО.
    Поддерживает все CRUD-операции с массовыми действиями.
    GET-запросы кешируются. Фильтрация по machine_id, status, priority, датам.
    """
    serializer_class = MaintenanceScheduleSerializer
    queryset = MaintenanceSchedule.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        machine_id = self.request.query_params.get('machine_id')
        status_param = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        scheduled_from = self.request.query_params.get('scheduled_from')
        scheduled_to = self.request.query_params.get('scheduled_to')

        if machine_id:
            qs = qs.filter(machine_id=machine_id)
        if status_param:
            qs = qs.filter(status=status_param)
        if priority:
            qs = qs.filter(priority=priority)
        if scheduled_from:
            qs = qs.filter(scheduled_date__gte=scheduled_from)
        if scheduled_to:
            qs = qs.filter(scheduled_date__lte=scheduled_to)
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одного или нескольких графиков ТО."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-обновление одного или нескольких графиков ТО."""
        many = isinstance(request.data, list)
        if many:
            instances = [MaintenanceSchedule.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одного или нескольких графиков ТО."""
        many = isinstance(request.data, list)
        if many:
            instances = [MaintenanceSchedule.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одного или нескольких графиков ТО (?ids=1,2,3)."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            MaintenanceSchedule.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)