from rest_framework.routers import DefaultRouter #Depende de la ruta el viewset que usemos
from core.api.views.core_views import PropertyViewSet
from core.api.views.general_views import *

router = DefaultRouter()

router.register(r'properties', PropertyViewSet, basename='properties')
#router.register(r'property_filter', PropertyList, basename='property_filter')
router.register(r'booking', BookingViewSet, basename='booking')
router.register(r'pricing_rule', PricingRuleViewSet, basename='pricing_rule')
#router.register(r'category-products', CategoryProductViewSet, basename='category_products')

urlpatterns = router.urls
