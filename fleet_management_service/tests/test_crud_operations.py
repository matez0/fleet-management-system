from http import HTTPStatus
from unittest.mock import ANY

from django.conf import settings
from django.test import Client, TestCase


class TestEndpointMixin:
    def setUp(self):
        self.client = Client()

    def test_crud_operations(self):
        item_id = self.check_create()

        self.check_update(item_id)

        self.check_retrieve(item_id)

        self.check_delete(item_id)

    def check_create(self):
        response = self.client.post(self.base_path, self.item)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json(), {**self.item, **{'id': ANY}})

        return response.json()['id']

    def check_update(self, item_id):
        response = self.client.put(f'{self.base_path}{item_id}/', self.updated_item, content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def check_retrieve(self, item_id):
        response = self.client.get(f'{self.base_path}{item_id}/')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {**self.updated_item, **{'id': item_id}})

    def check_delete(self, item_id):
        response = self.client.delete(f'{self.base_path}{item_id}/')

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

        response = self.client.get(f'{self.base_path}{item_id}/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestVehicleEndpoint(TestEndpointMixin, TestCase):
    base_path = '/vehicle/'
    item = {"type": "yacht", "registration": "CY1234"}
    updated_item = {"type": "boat", "registration": "XC5678"}


class TestDriverEndpoint(TestEndpointMixin, TestCase):
    base_path = '/driver/'
    item = {"fullName": "Sarah Connor", "points": 123}
    updated_item = {"fullName": "John Connor", "points": 45}


class TestTripEndpoint(TestEndpointMixin, TestCase):
    base_path = '/trip/'
    item = {"depatureGeoPoint": 12, "destinationGeoPoint": 34}
    updated_item = {"depatureGeoPoint": 56, "destinationGeoPoint": 78}


class TestAssignementEndpointMixin(TestEndpointMixin):
    def setUp(self):
        super().setUp()

        self.item = self.create_item()
        self.updated_item = self.create_item()

    def create_item_id(self, obj):
        response = self.client.post(obj.base_path, obj.item)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        return response.json()['id']


class TestDriverToVehicleEndpoint(TestAssignementEndpointMixin, TestCase):
    base_path = '/driver-to-vehicle/'

    def create_item(self):
        return {
            "driver": self.create_item_id(TestDriverEndpoint),
            "vehicle": self.create_item_id(TestVehicleEndpoint),
        }


class TestVehicleToTripEndpoint(TestAssignementEndpointMixin, TestCase):
    base_path = '/vehicle-to-trip/'

    def create_item(self):
        return {
            "trip": self.create_item_id(TestTripEndpoint),
            "vehicle": self.create_item_id(TestVehicleEndpoint),
        }
