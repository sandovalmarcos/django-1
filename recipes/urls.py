# from django.contrib import admin
from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name="home"),
    path('recipes/search/', views.search, name="search"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
    path('recipes/category/<int:category_id>/', views.category, name="category"), # noqa E501
]
