# from django.contrib import admin
from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('',
         views.RecipeListViewHome.as_view(),
         name="home"),
    path('recipes/api/v1/',
         views.RecipeListViewHomeApi.as_view(),
         name="recipes_api_v1"),
    path('recipes/search/',
         views.RecipeListViewSearch.as_view(),
         name="search"),
    path('recipes/<int:pk>/',
         views.RecipeDetailView.as_view(),
         name="recipe"),
    path('recipes/api/v1/<int:pk>/',
         views.RecipeDetailAPI.as_view(),
         name="recipes_api_v1_detail"),
    path('recipes/category/<int:category_id>/',
         views.RecipeListViewCategory.as_view(),
         name="category"),
    path('recipes/category/<int:category_id>/',
         views.RecipeListViewCategory.as_view(),
         name="category"),
]
