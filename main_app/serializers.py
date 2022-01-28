from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserFriend

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['username','id', 'email']


class UserFriendSerializer (serializers.ModelSerializer):
    class Meta: 
        model = UserFriend
        fields = '__all__'
