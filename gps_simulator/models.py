from django.db import models


class TripState(models.Model):
    driverId = models.UUIDField()
    vehicleId = models.UUIDField()
    speed = models.IntegerField()
    currentGeoPoint = models.IntegerField()
    destinationGeoPoint = models.IntegerField()
