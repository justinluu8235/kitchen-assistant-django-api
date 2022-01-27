from django.shortcuts import render
from django.contrib.auth.models import User
from .models import PantryCategory, PantryItem, ShoppingListItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
            by_category[serializer.data[i]['pantry_category']].append([serializer.data[i]])
        else:
            by_category[serializer.data[i]['pantry_category']] = [serializer.data[i]]
        
    print('organized by category', by_category)
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

    new_pantry_item = PantryItem.objects.create(item_name=item_name, user = user, pantry_category=pantry_category[0], in_stock=False)
    print('pantry item created', new_pantry_item)
    new_pantry_item.save()

    pantry_item_serializer = PantryItemSerializer(new_pantry_item , many=False)
    pantry_category_serializer = PantryCategorySerializer(pantry_category[0], many=False)
    obj={
        'pantry_item': pantry_item_serializer.data,
        'pantry_category': pantry_category_serializer.data,
    }
    return Response(obj)
