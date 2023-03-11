from django.db import transaction
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
import json
from .serializers import RecipeSerializer, RecipeStepSerializer, RecipeCategorySerializer, IngredientSerializer
from .models import Ingredient, Recipe, RecipeCategory, RecipeStep
from rest_framework.response import Response
from .helpers.recipe_helpers import clean_instructions, clean_ingredients

class RecipeCreate(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @transaction.atomic
    def post(self, request, format=None):
        instructions_list = json.loads(request.data['instructions_list'])
        ingredients_list = json.loads(request.data['ingredients_list'])
        recipe_categories = json.loads(request.data['recipe_categories'])
        cleaned_instructions: list(str) = clean_instructions(instructions_list)
        cleaned_ingredients: list(object) = clean_ingredients(ingredients_list)
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            # saving the recipe to get it to serialize the FileUpload object for the image
            recipe = serializer.save()
            categories = []
            for category_name in recipe_categories:
                recipe_category, created = RecipeCategory.objects.get_or_create(
                    category_name=category_name, user=recipe.user)
                categories.append(recipe_category)
            recipe = Recipe.objects.get(pk=recipe.id)
            recipe.categories.set(categories)
            if recipe.image and str(recipe.image) != '':
                recipe.image = 'https://res.cloudinary.com/djtd4wqoc/image/upload/v1643515599/' + str(recipe.image)
            recipe.save()
            for step_index, instructions in enumerate(cleaned_instructions):
                step_number = step_index
                recipe_step = recipe.steps.create(step_number=step_number,
                                                  instructions=instructions,
                                                  image=None, recipe=recipe)
            for ingredients in cleaned_ingredients:
                parsed_ingredient_name = ingredients['ingredient_name'].lower().strip()
                parsed_quantity_unit = ingredients['quantity_unit'].lower().strip()
                ingredient = recipe.ingredients.create(ingredient_name=parsed_ingredient_name,
                                                       ingredient_quantity=str(
                                                           round(float(ingredients['ingredient_quantity']), 2)),
                                                       quantity_unit=parsed_quantity_unit, recipe=recipe)

            recipe_serializer = RecipeSerializer(recipe, many=False)
            recipe_categories_serializer = RecipeCategorySerializer(categories, many=True)
            instructions_serializer = RecipeStepSerializer(RecipeStep.objects.filter(recipe=recipe), many=True)
            ingredients_serializer = IngredientSerializer(Ingredient.objects.filter(recipe=recipe), many=True)
            obj = {
                'recipe': recipe_serializer.data,
                'recipe_categories': recipe_categories_serializer.data,
                'instructions': instructions_serializer.data,
                'ingredients': ingredients_serializer.data,
            }
            return Response(obj)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
