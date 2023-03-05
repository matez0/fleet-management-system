from rest_framework import viewsets

from .models import Driver, DriverToVehicle, Trip, Vehicle, VehicleToTrip
from .serializers import (
    DriverSerializer,
    DriverToVehicleSerializer,
    TripSerializer,
    VehicleSerializer,
    VehicleToTripSerializer,
)


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()


class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()


class DriverToVehicleViewSet(viewsets.ModelViewSet):
    serializer_class = DriverToVehicleSerializer
    queryset = DriverToVehicle.objects.all()


class VehicleToTripViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleToTripSerializer
    queryset = VehicleToTrip.objects.all()
