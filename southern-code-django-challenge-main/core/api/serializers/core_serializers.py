
from rest_framework import serializers

from core.models import Properties,PricingRule,Booking

class PropertySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Properties
        exclude = ()

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'base_price':instance.base_price,
        }
    
    
class PropertyRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Properties
        exclude = ()
