from rest_framework import serializers
from .models import PantryCategory, PantryItem, ShoppingListItem


class PantryCategorySerializer (serializers.ModelSerializer):
    class Meta: 
        model = PantryCategory
        fields = '__all__'

class PantryItemSerializer(serializers.ModelSerializer):
    pantry_category = serializers.SerializerMethodField()

    class Meta:
        model = PantryItem
        fields = ('id', 'item_name', 'in_stock', 'pantry_category', 'user')

    def get_pantry_category(self, obj):
        return obj.pantry_category.category_name

class ShoppingListItemSerializer (serializers.ModelSerializer):
    class Meta: 
        model = ShoppingListItem
        fields = '__all__'
