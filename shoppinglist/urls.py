from django.urls import path

from . import views

app_name='shoppinglist'
urlpatterns = [
    path('', views.index, name='index'),
    path('newPantryItem', views.pantry_new, name="pantry-new"),
    path('new', views.shoppingitem_new, name="sahoppingitem_new"),
    path('pantry/<int:id>', views.pantry_index, name="pantry-index"),
    path('<int:id>', views.shoppinglist_index, name="shoppinglist-index"),
    path('pantry/delete/<int:id>', views.pantry_delete, name="pantry-delete"),
    path('delete/<int:id>', views.shoppingitem_delete, name="shoppinglist-delete"),
    path('pantry/edit/<int:id>', views.pantry_edit, name="pantry-edit"),
    path('generate', views.shoppinglist_generate, name="shoppinglist_generate"),
]