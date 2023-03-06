from django.core.management.base import BaseCommand

from gps_simulator.events import start_consuming_start_trip_events


class Command(BaseCommand):
    def handle(self, *args, **options):
        start_consuming_start_trip_events()
