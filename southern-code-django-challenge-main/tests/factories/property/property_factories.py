from faker import Faker

from core.models import Properties

faker = Faker()

class PropertiesFactory():

    def build_property_JSON(self):
        return {
            'name': str(faker.name()),
            'base_price': 10,
        }

    def create_property(self):
        return Properties.objects.create(**self.build_property_JSON())