from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recipe, RecipeCategory, RecipeStep
import json
from .serializers import RecipeSerializer
import requests
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")

@api_view(['GET'])
@login_required
def recipe_index(request, username):
    user = User.objects.get(username=username)
    recipe_list = Recipe.objects.filter(user=user)
    serializer = RecipeSerializer(recipe_list, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def search_recipe(request):
    search_query = request.data['searchVal']
    # print('query:', search_query)
    # print('API_KEY:', API_KEY)
    queryResultsQuantity = 5
    url = 'https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={API_KEY}&number={queryResultsQuantity}'
    url = url.format(query=search_query, API_KEY=API_KEY, queryResultsQuantity=queryResultsQuantity )
    response = requests.get(url)
    response = response.json()['results']
    # print("API Results", response)
    #parse API data
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
    # print('Parsed Data', obj)
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
    recipe_title = response['title']
    recipe_image = response['image']
    ingredientArr = list(map(parse_ingredients, response['extendedIngredients'] ))
    print(ingredientArr)

    url = 'https://api.spoonacular.com/recipes/{apiRecipeId}/analyzedInstructions?apiKey={API_KEY}'
    url = url.format(apiRecipeId=apiRecipeId, API_KEY=API_KEY)
    response = requests.get(url)
    response = response.json()
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
            'ingredient_quant': ingredient["amount"],
            'ingredient_unit': ingredient['unit']
        }
    return parsed_ingredient

def parse_instructions(instructions):
    parsed_instructions = {
            'step_number': instructions['number'],
            'instruction': instructions["step"],
        }
    return parsed_instructions