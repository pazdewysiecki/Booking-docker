from django.urls import path,re_path
from django.shortcuts import render
from core.api.views.core_views import PropertyList

urlpatterns = [
    path('filter/', PropertyList.as_view(), name = 'filter'),
    
  ]
