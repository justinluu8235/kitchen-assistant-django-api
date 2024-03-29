from django.urls import path
from . import views
from .recipe_create import RecipeCreate

app_name='recipes'
urlpatterns = [
    path('<int:id>', views.recipe_index, name='index'),
    path('searchRecipes/', views.search_recipe, name="search-recipe-index"),
    path('searchRecipes/<int:id>', views.search_recipe_view, name="view-search-recipe"),
    path('searchRecipes/new',  views.recipe_search_new, name="new-search-recipe"),
    path('new', RecipeCreate.as_view(), name="new-recipe"),
    path('view/<int:id>', views.recipe_show, name="show-recipe"),
    path('edit/<int:id>', views.recipe_edit, name="edit-recipe"),
    path('delete/<int:id>', views.recipe_delete, name="delete-recipe"),
    path('categories/<int:user_id>', views.categories_get, name="get-categories"),
]

