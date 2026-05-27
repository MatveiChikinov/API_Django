from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgriculturalMachineViewSet, MaintenanceScheduleViewSet

router = DefaultRouter()
router.register(r'machines', AgriculturalMachineViewSet, basename='machine')
router.register(r'maintenances', MaintenanceScheduleViewSet, basename='maintenance')

urlpatterns = [
    path('', include(router.urls)),
]