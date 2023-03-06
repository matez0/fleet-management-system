from time import sleep

from if_fms_gs import ROUTING_KEY_START_TRIP, StartTripMessage
from if_gs_vms import GpsMessage, ROUTING_KEY_GPS, TIME_DIFF, ACC
from messaging import Callback, send_message, start_consumer
from .models import TripState
from .trip import iter_motion

logger = logging.getLogger('django')


def emit_gps_events():
    while True:
        for trip_state in TripState.objects.all():
            send_message(
                ROUTING_KEY_GPS,
                GpsMessage(
                    driverId=str(trip_state.driverId),
                    vehicleId=str(trip_state.vehicleId),
                    speed=trip_state.speed,
                    currentGeoPoint=trip_state.currentGeoPoint,
                    destinationGeoPoint=trip_state.destinationGeoPoint,
                )
            )
            if trip_state.currentGeoPoint == trip_state.destinationGeoPoint:
                trip_state.delete()
                continue

            pos, step = iter_motion(
                trip_state.currentGeoPoint - trip_state.destinationGeoPoint, trip_state.speed * TIME_DIFF, ACC
            )
            trip_state.currentGeoPoint = trip_state.destinationGeoPoint + pos
            trip_state.speed = step // TIME_DIFF
            trip_state.save()

        sleep(2)


def start_consuming_start_trip_events():
    start_consumer(ROUTING_KEY_START_TRIP, start_trip)


@Callback(StartTripMessage)
def start_trip(message: StartTripMessage, header):
    TripState(
        driverId=message.driverId,
        vehicleId=message.vehicleId,
        speed=0,
        currentGeoPoint=message.depatureGeoPoint,
        destinationGeoPoint=message.destinationGeoPoint,
    ).save()
