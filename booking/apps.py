from django.apps import AppConfig


class BookingConfig(AppConfig):
    name = 'booking'

    def ready(self):
        from booking.models import Hotel, fake_db
        if Hotel.objects.count() == 0:
            fake_db()
