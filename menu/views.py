from django.shortcuts import render
from rest_framework.decorators import api_view

from recipes.serializers import RecipeSerializer
from  .serializers import MenuItemSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import MenuItem
from recipes.models import Recipe


@api_view(['GET'])
def menu_index(request, id):
    print('user id', id)
    user = User.objects.get(pk=id)
    print('user', user)
    menu_list = MenuItem.objects.filter(user=user)
    serializer = MenuItemSerializer(menu_list, many=True)

    by_date = {}
    for i in range(len(serializer.data)):
        recipeId = serializer.data[i]['recipe']
        recipe = Recipe.objects.get(pk=recipeId)
        serializer.data[i]['recipe_name'] = recipe.recipe_name
        print("recipe name", recipe.recipe_name)
        print("recipe image", recipe.image)
        serializer.data[i]['image'] = str(recipe.image)
        if serializer.data[i]['cook_date'] in by_date:
            cook_date = serializer.data[i]['cook_date']
            by_date[cook_date].append(serializer.data[i])
        else:
            cook_date = serializer.data[i]['cook_date']
            by_date[cook_date] = []
            by_date[cook_date].append(serializer.data[i])

    return Response(by_date)


@api_view(['POST'])
def menu_new(request):
    print(request.data)
    recipe_owner_id = request.data['recipe_owner_id']
    cook_date = request.data['cook_date']
    recipe_id = request.data['recipe_id']
    requester_username = request.data['requester_username']

    recipe_owner = User.objects.get(pk=recipe_owner_id)
    print("user:", recipe_owner)

    recipe = Recipe.objects.get(pk=recipe_id)
    print('recipe', recipe)

    menu_item = MenuItem.objects.create(cook_date=cook_date, recipe=recipe, 
                            user=recipe_owner, requester_username=requester_username)

    menu_item.save()

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
    print('menu item', menu_item)
    menu_item.delete()

    return Response("Item successfully deleted")


