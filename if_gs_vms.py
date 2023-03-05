from pydantic import BaseModel

ROUTING_KEY_GPS = 'fms.gps'

GeoPoint = int


class GpsMessage(BaseModel):
    driverId: str
    vehicleId: str
    speed: int
    currentGeoPoint: GeoPoint
    destinationGeoPoint: GeoPoint
