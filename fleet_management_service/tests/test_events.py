from http import HTTPStatus

from django.test import Client, TestCase

from if_fms_gs import ROUTING_KEY_START_TRIP, StartTripMessage
from messaging.main import create_channel_prepared_for_consuming


def consume_message(routing_key: str, message_type, timeout=5):
    with create_channel_prepared_for_consuming(routing_key) as channel:
        for _, _, body in channel.consume(routing_key, inactivity_timeout=timeout, auto_ack=True):
            assert body is not None
            message = message_type.parse_raw(body)
            channel.cancel()

        return message


def purge_message_queue(routing_key: str):
    with create_channel_prepared_for_consuming(routing_key) as channel:
        channel.queue_purge(routing_key)


class TestEvents(TestCase):
    def setUp(self):
        self.client = Client()

        self.driver_id = self.create_item('/driver/', {"fullName": "Sarah Connor", "points": 123})
        self.vehicle_id = self.create_item('/vehicle/', {"type": "yacht", "registration": "CY1234"})
        self.departure = 12
        self.destination = 34
        self.trip_id = self.create_item(
            '/trip/', {"depatureGeoPoint": self.departure, "destinationGeoPoint": self.destination}
        )

        purge_message_queue(ROUTING_KEY_START_TRIP)

    def create_item(self, base_path, item):
        response = self.client.post(base_path, item)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        return response.json()['id']

    def check_start_trip_message_sent(self):
        self.assertEqual(
            consume_message(ROUTING_KEY_START_TRIP, StartTripMessage),
            StartTripMessage(
                driverId=self.driver_id,
                vehicleId=self.vehicle_id,
                depatureGeoPoint=self.departure,
                destinationGeoPoint=self.destination,
            )
        )

    def test_assigning_trip_after_assigning_driver_triggers_start_trip_message(self):
        self.create_item('/driver-to-vehicle/', {"driver": self.driver_id, "vehicle": self.vehicle_id})
        self.create_item('/vehicle-to-trip/', {"trip": self.trip_id, "vehicle": self.vehicle_id})

        self.check_start_trip_message_sent()

    def test_assigning_driver_after_assigning_trip_triggers_start_trip_message(self):
        self.create_item('/vehicle-to-trip/', {"trip": self.trip_id, "vehicle": self.vehicle_id})
        self.create_item('/driver-to-vehicle/', {"driver": self.driver_id, "vehicle": self.vehicle_id})

        self.check_start_trip_message_sent()
