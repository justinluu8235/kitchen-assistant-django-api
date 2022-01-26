from django.urls import path
from . import views

app_name='recipes'
urlpatterns = [
    path('', views.recipe_index, name='index'),
    path('searchRecipes/', views.search_recipe, name="search-recipe-index"),
    path('searchRecipes/<int:id>', views.search_recipe_view, name="view-search-recipe")
]