from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('search/', search, name='search'),
    path('result/', ajax_pub, name='result'),
    path('list/', search_result, name='list'),
    path('list/result/', ajax_pubs, name='list_result'),
    path('save-cite/', save_cite, name='save_cite'),
    path('', cite, name='cite'),
]