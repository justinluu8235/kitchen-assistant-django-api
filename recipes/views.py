
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ingredient, Recipe, RecipeCategory, RecipeStep
import json
from .serializers import RecipeSerializer, RecipeStepSerializer, RecipeCategorySerializer, IngredientSerializer
import requests
from dotenv import load_dotenv
import os
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView


load_dotenv()
API_KEY = os.getenv("API_KEY")

@api_view(['GET'])
def recipe_index(request, id):
    print('user id', id)
    user = User.objects.get(pk=id)
    print('user', user)
    recipe_list = Recipe.objects.filter(user=user)
    serializer = RecipeSerializer(recipe_list, many=True)
    print(serializer.data)
    return Response(serializer.data)



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


@api_view(['get'])
def search_recipe_view(request, id):
    print("Spoonacular Recipe ID:", id)
    apiRecipeId = id
    url = 'https://api.spoonacular.com/recipes/{apiRecipeId}/information?apiKey={API_KEY}&includeNutrition=false'
    url = url.format(apiRecipeId=apiRecipeId, API_KEY=API_KEY)
    response = requests.get(url)
    response = response.json()
    print(response)
    recipe_title = response['title']
    recipe_image = response['image']
    ingredientArr = list(map(parse_ingredients, response['extendedIngredients'] ))
    print(ingredientArr)

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
    data=json.dumps(obj)
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



@api_view(['GET'])
def recipe_show(request, id):
    recipeId = id
    recipe = Recipe.objects.get(pk=id)
    print('recipe', recipe)
    recipe_category = RecipeCategory.objects.get(pk=recipe.recipe_category.id)
    print('recipecat' , recipe_category)
    ingredient_list = recipe.ingredient_set.all()
    instruction_list = recipe.recipestep_set.all()
    print('ingredients', ingredient_list)
    print('instructions', instruction_list)
    recipe_serializer = RecipeSerializer(recipe , many=False)
    instructions_serializer = RecipeStepSerializer(instruction_list, many=True)
    ingredients_serializer = IngredientSerializer(ingredient_list, many=True)
    recipe_category_serializer = RecipeCategorySerializer(recipe_category, many=False)
    obj={
        'recipe': recipe_serializer.data,
        'instructions': instructions_serializer.data,
        'ingredients': ingredients_serializer.data,
        'recipe_category': recipe_category_serializer.data,
    }
    print('response', obj)
    return Response(obj)


class RecipeCreate(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, format=None):

        print('requestdata', request.data)

        serializer = RecipeSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            print(serializer.data)



            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def recipe_new(request, format=None):
    user_id = request.data['user_id']
    recipe_id = request.data['recipe_id']
    recipe_category = request.data['recipe_category']
    instructions_list = request.data['instructions_list']
    ingredients_list = request.data['ingredients_list']

    user = User.objects.get(pk=user_id)
    print("user:", user)
    
    recipe_category = RecipeCategory.objects.get_or_create(category_name=recipe_category)
    print('recipe category', recipe_category)
    recipe_category[0].user = user
    recipe_category[0].save()

    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.recipe_category = recipe_category[0]
    print('recipe image' , str(recipe.image) == '' )
    if( recipe.image is not None and str(recipe.image) is not '' ):
        recipe.image = 'https://res.cloudinary.com/djtd4wqoc/image/upload/v1643515599/' + str(recipe.image) 
    
    recipe.user = user
    recipe.save()

    for instructions in instructions_list:
        recipe_step = recipe.recipestep_set.create(step_number=instructions['step_number'], 
                        instructions=instructions['instructions'], image=None, recipe=recipe)
        print(recipe_step)
        recipe_step.save()
    
    for ingredients in ingredients_list:
        print('ingredient unit before parse', ingredients['quantity_unit'])
        parsed_ingredient_name = ingredients['ingredient_name'].lower().strip()
        parsed_quantity_unit = ingredients['quantity_unit'].lower().strip()
        if(len(parsed_quantity_unit) > 1 and parsed_quantity_unit[-1] == 's' ):
            parsed_quantity_unit = parsed_quantity_unit[:-1]
        print('ingredient unit afetr parse', parsed_quantity_unit)
        print(type(int(ingredients['ingredient_quantity'])))
        ingredient = recipe.ingredient_set.create(ingredient_name=parsed_ingredient_name, 
                        ingredient_quantity=str(round(float(ingredients['ingredient_quantity']),2)), quantity_unit=parsed_quantity_unit, recipe=recipe)
        print(ingredient)
        ingredient.save()



    recipe_serializer = RecipeSerializer(recipe , many=False)
    recipe_category_serializer = RecipeCategorySerializer(recipe_category[0], many=False)
    instructions_serializer = RecipeStepSerializer(RecipeStep.objects.filter(recipe=recipe), many=True)
    ingredients_serializer = IngredientSerializer(Ingredient.objects.filter(recipe=recipe), many=True)
    obj={
        'recipe': recipe_serializer.data,
        'category': recipe_category_serializer.data,
        'instructions': instructions_serializer.data,
        'ingredients': ingredients_serializer.data,
    }
    # print(obj)
    # data=json.dumps(obj)
    return Response(obj)



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
    print(user_id)
    print(recipe_name)
    print(instructions_list)

    user = User.objects.get(pk=user_id)
    print("user:", user)
    
    recipe_category = RecipeCategory.objects.get_or_create(category_name=recipe_category)
    print('recipe category', recipe_category)
    recipe_category[0].user = user
    recipe_category[0].save()

    new_recipe = Recipe.objects.create(recipe_name=recipe_name, user = user, recipe_category=recipe_category[0], image=recipe_image)
    print('recipe created', new_recipe)
    new_recipe.save()

    for instructions in instructions_list:
        recipe_step = new_recipe.recipestep_set.create(step_number=instructions['step_number'], 
                        instructions=instructions['instructions'], image=None, recipe=new_recipe)
        print(recipe_step)
        recipe_step.save()
    
    for ingredients in ingredients_list:
        print('ingredient unit before parse', ingredients['quantity_unit'])
        parsed_ingredient_name = ingredients['ingredient_name'].lower().strip()
        parsed_quantity_unit = ingredients['quantity_unit'].lower().strip()
        if(len(parsed_quantity_unit) > 1 and parsed_quantity_unit[-1] == 's' ):
            parsed_quantity_unit = parsed_quantity_unit[:-1]
        print('ingredient unit afetr parse', parsed_quantity_unit)
        ingredient = new_recipe.ingredient_set.create(ingredient_name=parsed_ingredient_name, 
                        ingredient_quantity=str(round(float(ingredients['ingredient_quantity']),2)), quantity_unit=parsed_quantity_unit, recipe=new_recipe)
        print(ingredient)
        ingredient.save()



    recipe_serializer = RecipeSerializer(new_recipe , many=False)
    recipe_category_serializer = RecipeCategorySerializer(recipe_category[0], many=False)
    instructions_serializer = RecipeStepSerializer(RecipeStep.objects.filter(recipe=new_recipe), many=True)
    ingredients_serializer = IngredientSerializer(Ingredient.objects.filter(recipe=new_recipe), many=True)
    obj={
        'recipe': recipe_serializer.data,
        'category': recipe_category_serializer.data,
        'instructions': instructions_serializer.data,
        'ingredients': ingredients_serializer.data,
    }
    # print(obj)
    # data=json.dumps(obj)
    return Response(obj)
    



class RecipeEdit(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, format=None):

        print('requestdata', request.data)

        recipe_id = request.data['id']
        image_file = request.data['image']
        print('image file', image_file)
        recipe = Recipe.objects.get(pk=recipe_id)
        print('image before', recipe.image)
        recipe.image = image_file
   
        recipe.save()
        print('after save', recipe.image)
        recipe.image = 'https://res.cloudinary.com/djtd4wqoc/image/upload/v1643515599/' + str(recipe.image) 
        recipe.save()
        print('image after', recipe.image)
        serializer = RecipeSerializer(recipe, many=False)

        print('serializer data', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def recipe_edit(request, id):
    user_id = request.data['user_id']
    recipe_name = request.data['recipe_name']
    recipe_category = request.data['recipe_category']
    instructions_list = request.data['instructions_list']
    ingredients_list = request.data['ingredients_list']
    print(user_id)
    print(recipe_name)
    print(instructions_list)

    user = User.objects.get(pk=user_id)
    print("user:", user)

    recipe = Recipe.objects.get(pk=id)
    print('recipe image', recipe.image)
    if( recipe.image != None and str(recipe.image) != '' ):
        
        recipe.image = 'https://res.cloudinary.com/djtd4wqoc/image/upload/v1643515599/' + str(recipe.image) 
        print('after concat', recipe.image)
    recipe_category = RecipeCategory.objects.get_or_create(category_name=recipe_category)
    print('recipe category', recipe_category)
    recipe_category[0].save()
    
    recipe.recipe_category = recipe_category[0]
    recipe.save()

    print('update recipe', recipe)
    print('after update recipe', recipe.image)
    recipe.recipestep_set.all().delete()
    for instructions in instructions_list:
        recipe_step = recipe.recipestep_set.create(step_number=instructions['step_number'], 
                        instructions=instructions['instructions'], image=None, recipe=recipe)
        print(recipe_step)
        recipe_step.save()
    recipe.ingredient_set.all().delete()
    for ingredients in ingredients_list:
        print('ingredient unit before parse', ingredients['quantity_unit'])
        parsed_ingredient_name = ingredients['ingredient_name'].lower().strip()
        parsed_quantity_unit = ingredients['quantity_unit'].lower().strip()
        if(len(parsed_quantity_unit) > 1 and parsed_quantity_unit[-1] == 's' ):
            parsed_quantity_unit = parsed_quantity_unit[:-1]
        print('ingredient unit afetr parse', parsed_quantity_unit)
        ingredient = recipe.ingredient_set.create(ingredient_name=parsed_ingredient_name, 
                        ingredient_quantity=str(round(float(ingredients['ingredient_quantity']),2)), quantity_unit=parsed_quantity_unit, recipe=recipe)
        print(ingredient)
        ingredient.save()



    recipe_serializer = RecipeSerializer(recipe , many=False)
    recipe_category_serializer = RecipeCategorySerializer(recipe_category[0], many=False)
    instructions_serializer = RecipeStepSerializer(RecipeStep.objects.filter(recipe=recipe), many=True)
    ingredients_serializer = IngredientSerializer(Ingredient.objects.filter(recipe=recipe), many=True)
    obj={
        'recipe': recipe_serializer.data,
        'category': recipe_category_serializer.data,
        'instructions': instructions_serializer.data,
        'ingredients': ingredients_serializer.data,
    }
    # print(obj)
    # data=json.dumps(obj)
    return Response(obj)


@api_view(['DELETE'])
def recipe_delete(request, id):
    recipe = Recipe.objects.get(id=id)
    recipe.delete()

    return Response("Item successfully deleted")