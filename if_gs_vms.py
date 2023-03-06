from pydantic import BaseModel

ROUTING_KEY_GPS = 'fms.gps'

# Time and second position difference (acceleration) units:
TIME_DIFF = 3
ACC = 10

GeoPoint = int


class GpsMessage(BaseModel):
    driverId: str
    vehicleId: str
    speed: int
    currentGeoPoint: GeoPoint
    destinationGeoPoint: GeoPoint
