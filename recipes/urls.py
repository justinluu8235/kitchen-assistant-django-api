from django.urls import path
from . import views

app_name='recipes'
urlpatterns = [
    path('<int:id>', views.recipe_index, name='index'),
    path('searchRecipes/', views.search_recipe, name="search-recipe-index"),
    path('searchRecipes/<int:id>', views.search_recipe_view, name="view-search-recipe"),
    path('new', views.recipe_new, name="new-recipe"),
    path('recipeImage', views.recipe_add_image, name="addimage-recipe"),
    path('view/<int:id>', views.recipe_show, name="show-recipe"),
    path('edit/<int:id>', views.recipe_edit, name="edit-recipe"),
    path('delete/<int:id>', views.recipe_delete, name="delete-recipe"),
    
]