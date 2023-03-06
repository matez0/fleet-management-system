from django.core.management.base import BaseCommand

from vehicle_monitoring_system.events import start_consuming_gps_events


class Command(BaseCommand):
    def handle(self, *args, **options):
        start_consuming_gps_events()
