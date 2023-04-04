from django.urls import path

from . import views

app_name='menu'
urlpatterns = [
    path('index/<int:id>', views.menu_index, name='menu-index'),
    path('new', views.menu_new, name='menu-new'),
    path('delete/<int:id>', views.menu_delete, name='menu-delete'),
]