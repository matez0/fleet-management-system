from django.core.management.base import BaseCommand

from fleet_management_service.events import start_consuming_penalty_events


class Command(BaseCommand):
    def handle(self, *args, **options):
        start_consuming_penalty_events()
