from django.shortcuts import render
from rest_framework.decorators import api_view

from recipes.serializers import RecipeSerializer
from  .serializers import MenuItemSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import MenuItem
from recipes.models import Recipe
from main_app.auth_helpers import validate_token

# get all the menu items for a user
@api_view(['GET'])
def menu_index(request, id):
    user = User.objects.get(pk=id)

    try:
        validate_token(request.headers.get("Authorization"), user)
    except Exception as e:
        return Response(data={"error": "access denied..who are you?"}, status=400)

    menu_list = MenuItem.objects.filter(user=user)
    serializer = MenuItemSerializer(menu_list, many=True)

    by_date = {}
    for i in range(len(serializer.data)):
        recipeId = serializer.data[i]['recipe']
        recipe = Recipe.objects.get(pk=recipeId)
        serializer.data[i]['recipe_name'] = recipe.recipe_name

        serializer.data[i]['image'] = str(recipe.image)
        if serializer.data[i]['cook_date'] in by_date:
            cook_date = serializer.data[i]['cook_date']
            by_date[cook_date].append(serializer.data[i])
        else:
            cook_date = serializer.data[i]['cook_date']
            by_date[cook_date] = []
            by_date[cook_date].append(serializer.data[i])

    return Response(by_date)


# create a new menu item for a user
@api_view(['POST'])
def menu_new(request):
    recipe_owner_id = request.data['recipe_owner_id']
    cook_date = request.data['cook_date']
    recipe_id = request.data['recipe_id']
    requester_username = request.data['requester_username']
    meal_name = request.data.get("meal_name", "unknown")
    note = request.data.get("note", "")
    requester = User.objects.get(username=requester_username)

    try:
        validate_token(request.headers.get("Authorization"), requester)
    except Exception as e:
        return Response(data={"error": "access denied..who are you?"}, status=400)
    # TODO: make sure that the recipe owner is the requester's friend
    recipe_owner = User.objects.get(pk=recipe_owner_id)

    recipe = Recipe.objects.get(pk=recipe_id)

    menu_item = MenuItem.objects.create(cook_date=cook_date, recipe=recipe, 
                            user=recipe_owner, requester_username=requester_username,
                                        meal_name=meal_name, note=note)

    menu_item_serializer = MenuItemSerializer(menu_item, many=False)
    recipe_serializer = RecipeSerializer(recipe, many=False)
    obj={
        'menu_item': menu_item_serializer.data,
        'recipe': recipe_serializer.data,
    }
    return Response(obj)

@api_view(['DELETE'])
def menu_delete(request, id):
    menu_item = MenuItem.objects.get(id=id)
    user = menu_item.user

    try:
        validate_token(request.headers.get("Authorization"), user)
    except Exception as e:
        return Response(data={"error": "access denied..who are you?"}, status=400)

    menu_item.delete()
    return Response("Item successfully deleted")


