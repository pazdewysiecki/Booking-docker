from faker import Faker

from core.models import PricingRule

faker = Faker()


class PricingRuleFactory():
    #Rule one


    def build_pricing_rule_JSON(self, properties=None, price_modifier=None, min_stay_length=None):
        return {
            'properties': properties,
            'price_modifier': price_modifier,
            'min_stay_length': min_stay_length,
  
        }

    def create_pricing_rule(self):
        return PricingRule.objects.create(**self.build_pricing_rule_JSON())
    



class PricingRule_three_Factory():


    #Rule three

    def build_pricing_rule_JSON(self):
        return {
            'properties': 4,
            'fixed_price': 20,
            'specific_day': '2022-07-04',
        }

    def create_pricing_rule(self):
        return PricingRule.objects.create(**self.build_pricing_rule_JSON())