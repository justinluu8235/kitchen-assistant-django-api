from django.urls import path

from . import views

app_name='menu'
urlpatterns = [
    path('new', views.menu_new, name='menu-new'),
    path('index/<int:id>', views.menu_index, name='menu-index'),
    path('delete/<int:id>', views.menu_delete, name='menu-delete'),
    path('update/<int:id>', views.menu_update, name='menu-update'),
    path('<int:id>', views.menu_old_index, name='menu-old-index'),

]