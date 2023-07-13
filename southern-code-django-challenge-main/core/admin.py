from django.contrib import admin
from core.models import *

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price',)

class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ('properties', 'price_modifier','min_stay_length','fixed_price','specific_day',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('properties', 'date_start', 'date_end', 'final_price',)

# Register your models here.
admin.site.register(Properties,PropertyAdmin)
admin.site.register(PricingRule,PricingRuleAdmin)
admin.site.register(Booking,BookingAdmin)
