from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DriverViewSet, DriverToVehicleViewSet, TripViewSet, VehicleViewSet, VehicleToTripViewSet

router = DefaultRouter()
router.register(r"vehicle", VehicleViewSet)
router.register(r"driver", DriverViewSet)
router.register(r"trip", TripViewSet)
router.register(r"driver-to-vehicle", DriverToVehicleViewSet)
router.register(r"vehicle-to-trip", VehicleToTripViewSet)

urlpatterns = [
    path("", include(router.urls))
]
