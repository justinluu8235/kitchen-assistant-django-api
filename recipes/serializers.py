from rest_framework import serializers

from .models import Recipe, RecipeStep, RecipeCategory, Ingredient


class RecipeStepSerializer (serializers.ModelSerializer):
    class Meta: 
        model = RecipeStep
        fields = '__all__'

class RecipeCategorySerializer (serializers.ModelSerializer):
    class Meta: 
        model = RecipeCategory
        fields = '__all__'
        
class RecipeSerializer (serializers.ModelSerializer):
    categories = RecipeCategorySerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = '__all__'

class IngredientSerializer (serializers.ModelSerializer):
    class Meta: 
        model = Ingredient
        fields = '__all__'
        