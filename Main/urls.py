from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('search/', search, name='search'),
    path('paper/', paper, name='paper'),
    path('papers/', papers_result, name='papers'),
    path('papers/result/', send_pubs, name='papers_result'),
    path('create-citation/', create_citation, name='create_citation'),
    path('', index, name='index'),
]
