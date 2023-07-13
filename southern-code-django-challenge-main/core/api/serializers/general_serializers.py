from core.models import PricingRule,Booking

from rest_framework import serializers

class PricingRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PricingRule
        exclude = ()

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        exclude = ('final_price',)
     
    """
    def to_representation(self, instance):
        return {
            'properties': instance.properties.__str__(),
            'date_start': instance.date_start,
            'date_end': instance.date_end,
            'final_price': instance.final_price,
        }
        """
        

    

class BookingRetrievSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        exclude = ('final_price',)
     
    
    def to_representation(self, instance):
        return {
            'properties': instance.properties.name,
            'date_start':instance.date_start,
            'date_end':instance.date_end,
            'final_price':instance.final_price,
        }
        
        
        

