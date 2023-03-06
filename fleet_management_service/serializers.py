from rest_framework import serializers

from .models import Driver, DriverToVehicle, Trip, Vehicle, VehicleToTrip


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class DriverToVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverToVehicle
        fields = '__all__'


class VehicleToTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleToTrip
        fields = '__all__'
