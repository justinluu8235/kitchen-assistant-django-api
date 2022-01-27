from rest_framework import serializers
from .models import PantryCategory, PantryItem, ShoppingListItem


class PantryCategorySerializer (serializers.ModelSerializer):
    class Meta: 
        model = PantryCategory
        fields = '__all__'

class PantryItemSerializer (serializers.ModelSerializer):
    class Meta: 
        model = PantryItem
        fields = '__all__'

class ShoppingListItemSerializer (serializers.ModelSerializer):
    class Meta: 
        model = ShoppingListItem
        fields = '__all__'
