from core.models import Booking, PricingRule, Properties
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factories.booking.booking_factories import BookingFactory
from tests.factories.property.property_factories import PropertiesFactory
from tests.factories.pricing_rule.pricing_rule_factories import PricingRuleFactory


class BookingTestCase(APITestCase):
    
    #Creation of new property
    url = '/core/' 
    

    def test_a(self):
        property = PropertiesFactory().build_property_JSON()
        response = self.client.post(
            self.url + 'properties/',
            property,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Properties.objects.all().count(), 1)
    

class BookingTestCase_one(APITestCase):
    url = '/core/' 
    #CASE ONE

    def test_new_pricing_rule_one(self):
        print("Starting CASE ONE")

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

        properties= 2
        price_modifier=str(0.9)
        min_stay_length=7

        # pricing rule
        pricing_rule = PricingRuleFactory().build_pricing_rule_JSON(properties, price_modifier, min_stay_length)
        response = self.client.post(
            self.url + 'pricing_rule/',
            pricing_rule,
            format='json'
        )
   
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PricingRule.objects.all().count(), 1)

        #booking
        properties = 2

        booking = BookingFactory().build_booking_JSON(properties)
        response = self.client.post(
            self.url + 'booking/',
            booking,
            format='json'
        )
        

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.all().count(), 1)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.data['final_price'], 90)

class BookingTestCase_two(APITestCase):
    url = '/core/' 
    #CASE TWO

    def test_new_pricing_rule_two(self):
        print("Starting CASE TWO")
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

        properties= 3
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

        properties= 3
        price_modifier=str(0.8)
        min_stay_length=30

        # pricing rule two
        pricing_rule = PricingRuleFactory().build_pricing_rule_JSON(properties, price_modifier, min_stay_length)
        response = self.client.post(
            self.url + 'pricing_rule/',
            pricing_rule,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PricingRule.objects.all().count(), 2)

        #booking
        properties = 3

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
        self.assertEqual(response.data['final_price'], 90)












        