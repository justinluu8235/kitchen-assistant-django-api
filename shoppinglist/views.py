from django.shortcuts import render
from django.contrib.auth.models import User
from .models import PantryCategory, PantryItem, ShoppingListItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe
from .serializers import PantryCategorySerializer, PantryItemSerializer, ShoppingListItemSerializer
def index(request):
    template_name = 'shoppinglist/index.html'
    return template_name


@api_view(['GET'])
def pantry_index(request, id):
    print('user id', id)
    user = User.objects.get(pk=id)
    print('user', user)
    pantry_item_list = PantryItem.objects.filter(user=user).order_by('pantry_category')
    print('pantry list', pantry_item_list)
    serializer = PantryItemSerializer(pantry_item_list, many=True)
    print(serializer.data)
    by_category = {}
    for i in range(len(serializer.data)):
        if serializer.data[i]['pantry_category'] in by_category:
            category = serializer.data[i]['pantry_category']
            by_category[category].append(serializer.data[i])
            print('organized by category', by_category[category])
        else:
            category = serializer.data[i]['pantry_category']
            by_category[category] = []
            by_category[category].append(serializer.data[i])
            print('organized by category', by_category[category])
        
    # print('organized by category', by_category)
    return Response(by_category)
    

@api_view(['POST'])
def pantry_new(request):
    user_id = request.data['user_id']
    item_name = request.data['item_name']
    category_name = request.data['category_name']

    print('user id', user_id)
    print('item name', item_name)

    user = User.objects.get(pk=user_id)
    print("user:", user)

    pantry_category = PantryCategory.objects.get_or_create(category_name=category_name, user=user)
    print('pantry category', pantry_category)
    pantry_category[0].save()

    new_pantry_item = PantryItem.objects.create(item_name=item_name, user = user, pantry_category=pantry_category[0], in_stock=True)
    print('pantry item created', new_pantry_item)
    new_pantry_item.save()

    pantry_item_serializer = PantryItemSerializer(new_pantry_item , many=False)
    pantry_category_serializer = PantryCategorySerializer(pantry_category[0], many=False)
    obj={
        'pantry_item': pantry_item_serializer.data,
        'pantry_category': pantry_category_serializer.data,
    }
    return Response(obj)


@api_view(['POST'])
def pantry_edit(request, id):
    pantry_item = PantryItem.objects.get(id=id)
    pantry_item.in_stock = not pantry_item.in_stock
    pantry_item.save()

    if pantry_item.in_stock == False:
        shopping_item = ShoppingListItem.objects.create(item_name=pantry_item.item_name, user = pantry_item.user,
                                            ingredient_quantity=1, quantity_unit="pantry unit")
        shopping_item.save()
    


    return Response("Item successfully updated")

@api_view(['DELETE'])
def pantry_delete(request, id):
    pantry_item = PantryItem.objects.get(id=id)
    print('pantry_item', pantry_item)
    pantry_item.delete()

    return Response("Item successfully deleted")


@api_view(['GET'])
def shoppinglist_index(request, id):
    print('user id', id)
    user = User.objects.get(pk=id)
    print('user', user)
    shopping_item_list = ShoppingListItem.objects.filter(user=user)
    print('shopping list', shopping_item_list)
    serializer = ShoppingListItemSerializer(shopping_item_list, many=True)
    obj={
        'shopping_list': serializer.data,
    }
    print('response obj', obj)
    return Response(obj)


@api_view(['POST'])
def shoppingitem_new(request):
    user_id = request.data['user_id']
    item_name = request.data['item_name']
    item_quantity = request.data['item_quantity']
    quantity_unit = request.data['quantity_unit']

    print('user id', user_id)
    print('item name', item_name)

    user = User.objects.get(pk=user_id)
    print("user:", user)

    shopping_item = ShoppingListItem.objects.create(item_name=item_name, user = user,ingredient_quantity=item_quantity, quantity_unit=quantity_unit)
    shopping_item.save()

    shopping_item_serializer = ShoppingListItemSerializer(shopping_item, many=False)
    obj={
        'shopping_item': shopping_item_serializer.data,
    }
    print('response obj', obj)
    return Response(obj)


@api_view(['DELETE'])
def shoppingitem_delete(request, id):
    shopping_item = ShoppingListItem.objects.get(id=id)
    print('shopping item', shopping_item)
    shopping_item.delete()

    return Response("Item successfully deleted")





@api_view(['POST'])
def shoppinglist_generate(request):
    user_id = request.data['user_id']
    recipe_id = request.data['recipe_id']

    user = User.objects.get(pk=user_id)
    print('user', user)

    recipe = Recipe.objects.get(pk=recipe_id)
    print('recipe', recipe)

    ingredient_list = recipe.ingredient_set.all()
    print('ingredient list', ingredient_list)

    pantry_object_list = PantryItem.objects.all().filter(user=user)
    pantry_item_list = list(map(lambda pantry_object: pantry_object.item_name,pantry_object_list))
    print('pantry_item_list', pantry_item_list)

    for i in range(len(ingredient_list)):
        ingredient = ingredient_list[i]
        if not ingredient.ingredient_name in pantry_item_list:
            shopping_item = ShoppingListItem.objects.create(item_name=ingredient.ingredient_name, user = user,ingredient_quantity=ingredient.ingredient_quantity, 
                                                    quantity_unit=ingredient.quantity_unit)
            shopping_item.save()


    return Response("shopping list items successfully generated")

    