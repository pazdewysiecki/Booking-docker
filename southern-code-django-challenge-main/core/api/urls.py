from django.urls import path
from core.api.views.core_views import PropertyList


"""
urlpatterns = [
    path('usuario/', UsuarioAPIView.as_view(), name='usuario_api')
]
"""
urlpatterns = [
    path('property_list/', PropertyList.as_view(), name='property_list'),
]