from faker import Faker
from datetime import datetime, timedelta

from core.models import Booking

faker = Faker()


#Case 1 , Case 2 , Case 3




class BookingFactory():


    def build_booking_JSON(self, properties=None):
        return {
            'properties': properties,
            'date_start': '2022-07-01',
            'date_end': '2022-07-10',
        }

    def create_booking(self):
        return Booking.objects.create(**self.build_booking_JSON())
    

