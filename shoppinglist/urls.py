from django.urls import path

from . import views

app_name='shoppinglist'
urlpatterns = [
    path('', views.index, name='index'),
    path('newPantryItem', views.pantry_new, name="pantry-new"),
    path('pantry/<int:id>', views.pantry_index, name="pantry-index"),
]