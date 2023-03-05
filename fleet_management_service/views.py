from rest_framework import viewsets

from .events import start_trip_if_assigned, start_trip_if_driver_assigned
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

    def create(self, request):
        response = super().create(request)

        start_trip_if_assigned(request.data['driver'], request.data['vehicle'])

        return response


class VehicleToTripViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleToTripSerializer
    queryset = VehicleToTrip.objects.all()

    def create(self, request):
        response = super().create(request)

        start_trip_if_driver_assigned(request.data['vehicle'], request.data['trip'])

        return response
