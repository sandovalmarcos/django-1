from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from recipes.views import home, acerca, contacto

urlpatterns = [
    path('', home),
    path('acerca', acerca),
    path('contacto', contacto),
    
]
