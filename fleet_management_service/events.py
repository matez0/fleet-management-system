from if_fms_gs import StartTripMessage, ROUTING_KEY_START_TRIP
from if_vms_fms import PenaltyMessage, ROUTING_KEY_PENALTY
from messaging import Callback, send_message, start_consumer
from .models import Driver, DriverToVehicle, VehicleToTrip


def start_trip_if_assigned(driver_id, vehicle_id):
    try:
        trip = VehicleToTrip.objects.get(vehicle=vehicle_id).trip

    except VehicleToTrip.DoesNotExist:
        return

    _start_trip(driver_id, vehicle_id, trip)


def _start_trip(driver_id, vehicle_id, trip):
    send_message(
        ROUTING_KEY_START_TRIP,
        StartTripMessage(
            driverId=driver_id,
            vehicleId=vehicle_id,
            depatureGeoPoint=trip.depatureGeoPoint,
            destinationGeoPoint=trip.destinationGeoPoint,
        )
    )


def start_trip_if_driver_assigned(vehicle_id, trip_id):
    try:
        driver_id = str(DriverToVehicle.objects.get(vehicle=vehicle_id).driver.id)

    except DriverToVehicle.DoesNotExist:
        return

    trip = VehicleToTrip.objects.get(vehicle=vehicle_id).trip

    _start_trip(driver_id, vehicle_id, trip)


def start_consuming_penalty_events():
    start_consumer(ROUTING_KEY_PENALTY, add_penalty_points)


@Callback(PenaltyMessage)
def add_penalty_points(penalty: PenaltyMessage, header):
    driver = Driver.objects.get(id=penalty.driverId)
    driver.points += penalty.points
    driver.save()
