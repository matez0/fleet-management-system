from django.core.management.base import BaseCommand

from gps_simulator.events import emit_gps_events


class Command(BaseCommand):
    def handle(self, *args, **options):
        emit_gps_events()
