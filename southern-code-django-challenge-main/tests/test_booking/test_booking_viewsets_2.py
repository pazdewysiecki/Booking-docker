from core.models import Booking, PricingRule, Properties
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factories.booking.booking_factories import BookingFactory
from tests.factories.property.property_factories import PropertiesFactory
from tests.factories.pricing_rule.pricing_rule_factories import PricingRuleFactory, PricingRule_three_Factory

#CASE THREE

class BookingTestCase_three(APITestCase):
    url = '/core/' 
    

    def test_new_pricing_rule_three(self):
        print("Starting CASE THREE")
        #property
        property = PropertiesFactory().build_property_JSON()
        response = self.client.post(
            self.url + 'properties/',
            property,
            format='json'
        )
   
        #import pdb; pdb.set_trace()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Properties.objects.all().count(), 1)

        properties= 4
        price_modifier=str(0.9)
        min_stay_length=7

        # pricing rule one
        pricing_rule = PricingRuleFactory().build_pricing_rule_JSON(properties, price_modifier, min_stay_length)
        response = self.client.post(
            self.url + 'pricing_rule/',
            pricing_rule,
            format='json'
        )
        
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PricingRule.objects.all().count(), 1)


        # pricing rule three
        pricing_rule = PricingRule_three_Factory().build_pricing_rule_JSON()
        response = self.client.post(
            self.url + 'pricing_rule/',
            pricing_rule,
            format='json'
        )
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PricingRule.objects.all().count(), 2)

        #booking

        properties= 4

        booking = BookingFactory().build_booking_JSON(properties)
        response = self.client.post(
            self.url + 'booking/',
            booking,
            format='json'
        )
        
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.all().count(), 1)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.data['final_price'], 101)

