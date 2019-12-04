from django.core.management.base import BaseCommand

from booking.models import fake_db


class Command(BaseCommand):
    help = 'Fakes Hotels'

    def handle(self, *args, **options):
        fake_db()
