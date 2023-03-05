import uuid

from django.db import models


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=16)
    registration = models.CharField(max_length=16)


class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullName = models.CharField(max_length=100)
    points = models.IntegerField()


class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    depatureGeoPoint = models.IntegerField()
    destinationGeoPoint = models.IntegerField()


class DriverToVehicle(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)


class VehicleToTrip(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
