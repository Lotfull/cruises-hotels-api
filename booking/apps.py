from django.apps import AppConfig


class BookingConfig(AppConfig):
    name = 'booking'

    def ready(self):
        from django.db import connection
        if 'booking_hotel' in connection.introspection.table_names():
            from booking.models import Hotel, fake_db
            if Hotel.objects.count() == 0:
                 fake_db()
