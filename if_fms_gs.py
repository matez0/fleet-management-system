from pydantic import BaseModel

ROUTING_KEY_START_TRIP = 'fms.start-trip'

GeoPoint = int


class StartTripMessage(BaseModel):
    driverId: str
    vehicleId: str
    depatureGeoPoint: GeoPoint
    destinationGeoPoint: GeoPoint
