from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # path('user/<username>/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('name/<int:id>', views.get_name, name="get-name"),
    path('userFriends/<int:id>', views.userfriend_index, name="userfriend-index"),
    path('userFriends/search', views.userfriend_search, name="userfriend-search"),
    path('userFriends/add', views.userfriend_add, name="userfriend-add"),
    path('userFriends/accept', views.userfriend_accept, name="userfriend-accept"),
    path('userFriends/delete', views.userfriend_unfriend, name="userfriend-delete"),


]