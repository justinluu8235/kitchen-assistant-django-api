from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helpers.recipe_helpers import clean_instructions, clean_ingredients
from .models import Ingredient, Recipe, RecipeCategory, RecipeStep
import json
from .serializers import RecipeSerializer, RecipeStepSerializer, RecipeCategorySerializer, IngredientSerializer
import requests
from dotenv import load_dotenv
import os
import cloudinary.api
from django.conf import settings
from main_app.auth_helpers import validate_token

load_dotenv()
API_KEY = os.getenv("API_KEY")



# get all of a user's recipes
@api_view(['GET'])
def recipe_index(request, id):
    user = User.objects.get(pk=id)
    try:
        validate_token(request.headers.get("Authorization"), user, friend_access=True)
    except Exception as e:
        return Response(data={"error": "access denied..who are you?"}, status=400)

    recipe_list = Recipe.objects.filter(user=user)
    serializer = RecipeSerializer(recipe_list, many=True)
    print(serializer.data)
    return Response(serializer.data)

# search for recipes in the spoonacular API
@api_view(['POST'])
def search_recipe(request):
    search_query = request.data['searchVal']
    queryResultsQuantity = 10
    url = 'https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={API_KEY}&number={queryResultsQuantity}'
    url = url.format(query=search_query, API_KEY=API_KEY, queryResultsQuantity=queryResultsQuantity )
    response = requests.get(url)
    response = response.json()['results']
    recipeInfoArr = [None] * len(response)
    for i in range(len(response)):
        recipeInfoArr[i] = {
            'recipe_title': response[i]['title'],
            'recipe_id': response[i]["id"],
            'recipe_image_url': response[i]['image']
        }
    obj={
        'search_results': recipeInfoArr
    }
    data=json.dumps(obj)
    return Response(data)

# get info on one spoonacular recipe
@api_view(['get'])
def search_recipe_view(request, id):
    # spoonacular recipe id
    apiRecipeId = id
    url = 'https://api.spoonacular.com/recipes/{apiRecipeId}/information?apiKey={API_KEY}&includeNutrition=false'
    url = url.format(apiRecipeId=apiRecipeId, API_KEY=API_KEY)
    response = requests.get(url)
    response = response.json()
    recipe_title = response['title']
    recipe_image = response['image']
    ingredientArr = list(map(parse_ingredients, response['extendedIngredients'] ))

    url = 'https://api.spoonacular.com/recipes/{apiRecipeId}/analyzedInstructions?apiKey={API_KEY}'
    url = url.format(apiRecipeId=apiRecipeId, API_KEY=API_KEY)
    response = requests.get(url)
    response = response.json()
    if(len(response) < 1):
        instructionsArr = []
    else:
        response = response[0]['steps']
        instructionsArr = list(map(parse_instructions, response))

    obj={
        'recipe_title': recipe_title,
        'recipe_image': recipe_image,
        'ingredient_list': ingredientArr,
        'instructions_list': instructionsArr,
    }
    data = json.dumps(obj)
    return Response(data)


def parse_ingredients(ingredient):
    parsed_ingredient = {
            'ingredient_name': ingredient['name'],
            'ingredient_quantity': ingredient["amount"],
            'quantity_unit': ingredient['unit']
        }
    return parsed_ingredient

def parse_instructions(instructions):
    parsed_instructions = {
            'step_number': instructions['number'],
            'instructions': instructions["step"],
        }
    return parsed_instructions

# show one of a user's recipe
@api_view(['GET'])
def recipe_show(request, id):
    recipe = Recipe.objects.get(pk=id)
    recipe_owner = recipe.user

    try:
        validate_token(request.headers.get("Authorization"), recipe_owner, friend_access=True)
    except Exception as e:
        return Response(data={"error": "access denied..who are you?"}, status=400)

    recipe_categories = recipe.categories.all()
    ingredient_list = recipe.ingredients.all()
    instruction_list = recipe.steps.all().order_by('step_number')
    recipe_serializer = RecipeSerializer(recipe, many=False)
    instructions_serializer = RecipeStepSerializer(instruction_list, many=True)
    ingredients_serializer = IngredientSerializer(ingredient_list, many=True)
    recipe_categories_serializer = RecipeCategorySerializer(recipe_categories, many=True)
    obj = {
        'recipe': recipe_serializer.data,
        'instructions': instructions_serializer.data,
        'ingredients': ingredients_serializer.data,
        'recipe_categories': recipe_categories_serializer.data,
    }
    return Response(obj)

# return all categories for a user
@api_view(['GET'])
def categories_get(request, user_id):
    user = User.objects.get(pk=user_id)
    try:
        validate_token(request.headers.get("Authorization"), user, friend_access=True)
    except Exception as e:
        return Response(data={"error": "access denied..who are you?"}, status=400)

    categories = RecipeCategory.objects.filter(user_id=user_id).order_by('category_name')
    recipe_categories_serializer = RecipeCategorySerializer(categories, many=True)
    obj = {
        'recipe_categories': recipe_categories_serializer.data,
    }
    return Response(obj)


# create a new recipe for a user based off a spoonacular recipe
@transaction.atomic
@api_view(['POST'])
def recipe_search_new(request):
    user_id = request.data['user_id']
    recipe_name = request.data['recipe_name']
    recipe_category = request.data['recipe_category']
    instructions_list = request.data['instructions_list']
    ingredients_list = request.data['ingredients_list']

    recipe_image=None
    if 'recipe_image' in request.data:
        recipe_image = request.data['recipe_image']

    user = User.objects.get(pk=user_id)

    try:
        validate_token(request.headers.get("Authorization"), user)
    except Exception as e:
        return Response(data={"error": "access denied..who are you?"}, status=400)

    recipe_category, created = RecipeCategory.objects.get_or_create(
        category_name=recipe_category, user=user)

    new_recipe = Recipe.objects.create(
        recipe_name=recipe_name, user=user, image=recipe_image
    )
    new_recipe.categories.set([recipe_category.id])
    new_recipe.save()

    for instructions in instructions_list:
        recipe_step = new_recipe.steps.create(step_number=instructions['step_number'],
                        instructions=instructions['instructions'], image=None, recipe=new_recipe)
        print(recipe_step)
        recipe_step.save()
    
    for ingredients in ingredients_list:
        parsed_ingredient_name = ingredients['ingredient_name'].lower().strip()
        parsed_quantity_unit = ingredients['quantity_unit'].lower().strip()
        ingredient = new_recipe.ingredients.create(ingredient_name=parsed_ingredient_name,
                        ingredient_quantity=str(round(float(ingredients['ingredient_quantity']),2)), quantity_unit=parsed_quantity_unit, recipe=new_recipe)
        ingredient.save()


    recipe_serializer = RecipeSerializer(new_recipe , many=False)
    recipe_categories_serializer = RecipeCategorySerializer(new_recipe.categories.all(), many=False)
    instructions_serializer = RecipeStepSerializer(RecipeStep.objects.filter(recipe=new_recipe), many=True)
    ingredients_serializer = IngredientSerializer(Ingredient.objects.filter(recipe=new_recipe), many=True)
    obj={
        'recipe': recipe_serializer.data,
        'recipe_categories': recipe_categories_serializer.data,
        'instructions': instructions_serializer.data,
        'ingredients': ingredients_serializer.data,
    }
    # print(obj)
    # data=json.dumps(obj)
    return Response(obj)

# edit a user's existing recipe
@transaction.atomic
@api_view(['POST'])
def recipe_edit(request, id):
    user_id = request.data['user_id']
    user = User.objects.get(pk=user_id)

    try:
        validate_token(request.headers.get("Authorization"), user)
    except Exception as e:
        return Response(data={"error": "access denied..who are you?"}, status=400)


    recipe_name = request.data['recipe_name']
    recipe_categories = json.loads(request.data['recipe_categories'])
    instructions_list = json.loads(request.data['instructions_list'])
    ingredients_list = json.loads(request.data['ingredients_list'])
    image_file = request.data['image']
    user = User.objects.get(pk=user_id)
    cleaned_instructions: list(str) = clean_instructions(instructions_list)
    cleaned_ingredients: list(object) = clean_ingredients(ingredients_list)

    recipe = Recipe.objects.get(pk=id)
    categories = []
    for category_name in recipe_categories:
        recipe_category, created = RecipeCategory.objects.get_or_create(
            user=user, category_name=category_name)
        categories.append(recipe_category)
    recipe.categories.set(categories)
    recipe.recipe_name = recipe_name
    if image_file:
        _maybe_delete_cloudinary_image(recipe.image)
        recipe.image = image_file
        recipe.save()
        serialized_image_file = recipe.image
        cloudinary_upload_string = f'https://res.cloudinary.com/djtd4wqoc/image/upload/v1643515599/{str(serialized_image_file)}'
        recipe.image = cloudinary_upload_string

    recipe.save()
    recipe.steps.all().delete()
    for step_index, instructions in enumerate(cleaned_instructions):
        step_number = step_index + 1
        recipe_step = recipe.steps.create(step_number=step_number,
                        instructions=instructions, image=None, recipe=recipe)
        recipe_step.save()
    recipe.ingredients.all().delete()
    for ingredients in cleaned_ingredients:
        parsed_ingredient_name = ingredients['ingredient_name'].lower().strip()
        parsed_quantity_unit = ingredients['quantity_unit'].lower().strip()
        ingredient = recipe.ingredients.create(ingredient_name=parsed_ingredient_name,
                        ingredient_quantity=str(round(float(ingredients['ingredient_quantity']),2)), quantity_unit=parsed_quantity_unit, recipe=recipe)
        ingredient.save()

    recipe_serializer = RecipeSerializer(recipe , many=False)
    recipe_categories_serializer = RecipeCategorySerializer(categories, many=True)
    instructions_serializer = RecipeStepSerializer(RecipeStep.objects.filter(recipe=recipe), many=True)
    ingredients_serializer = IngredientSerializer(Ingredient.objects.filter(recipe=recipe), many=True)
    obj={
        'recipe': recipe_serializer.data,
        'recipe_categories': recipe_categories_serializer.data,
        'instructions': instructions_serializer.data,
        'ingredients': ingredients_serializer.data,
    }
    return Response(obj)

# delete a user's existing recipe
@api_view(['DELETE'])
def recipe_delete(request, id):
    recipe = Recipe.objects.get(id=id)
    user = recipe.user

    try:
        validate_token(request.headers.get("Authorization"), user)
    except Exception as e:
        return Response(data={"error": "access denied..who are you?"}, status=400)

    # if a cloudinary image, delete from cloudinary as well.
    _maybe_delete_cloudinary_image(recipe.image)
    recipe.delete()
    return Response("Item successfully deleted")

def _maybe_delete_cloudinary_image(recipe_image):
    if 'cloudinary' in str(recipe_image):
        # last part of path is the static id,
        # for ex: 'https://res.cloudinary.com/djtd4wqoc/image/upload/v1675476400/recipes/image_l3s21z'
        public_id = str(recipe_image).split('/').pop()
        delete_path = f'recipes/{public_id}'
        cloudinary_info = _get_cloudinary_info()
        try:
            response = cloudinary.api.delete_resources([delete_path], resource_type='image', **cloudinary_info)
            print(f'No issue deleting cloudinary image: {response}')
        except Exception as e:
            print(f'Error when deleting cloudinary image: {e}')

def _get_cloudinary_info() -> dict:
    info = {}
    info['cloud_name'] = settings.CLOUDINARY_STORAGE['CLOUD_NAME']
    info['api_key'] = settings.CLOUDINARY_STORAGE['API_KEY']
    info['api_secret'] = settings.CLOUDINARY_STORAGE['API_SECRET']
    return info