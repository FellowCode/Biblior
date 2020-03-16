from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
    path('personal-area/', personal_area, name='personal_area'),
    path('change-password/', change_password, name='change_password')
]
