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

    print('ingredient unit before parse', quantity_unit)
    parsed_ingredient_name = item_name.lower()
    parsed_quantity_unit = quantity_unit.lower()
    if(parsed_quantity_unit[-1] == 's'):
        parsed_quantity_unit = parsed_quantity_unit[:-1]
    print('ingredient unit afetr parse', parsed_quantity_unit)


    print('user id', user_id)
    print('item name', item_name)

    user = User.objects.get(pk=user_id)
    print("user:", user)

    shopping_item = ShoppingListItem.objects.create(item_name=parsed_ingredient_name, user = user,ingredient_quantity=item_quantity, quantity_unit=parsed_quantity_unit)
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
        print('pantry list', pantry_item_list)
        if not ingredient.ingredient_name in pantry_item_list:

            #see if the shopping list alreaady had the same ingredient
            print('checking for :', ingredient.ingredient_name)
            created_item = False
            shopping_item_exists = ShoppingListItem.objects.all().filter(user=user, item_name=ingredient.ingredient_name)
            print('list', shopping_item_exists)
            if(shopping_item_exists):
                for i in range(len(shopping_item_exists)):
                    print('item exists')
                    # existing_item = ShoppingListItem.objects.get(user=user, item_name=ingredient.ingredient_name)
                    existing_item = shopping_item_exists[i]
                    #if it does, get the unit, and convert the input unit to that unit
                    existing_quantity = existing_item.ingredient_quantity
                    existing_unit = existing_item.quantity_unit
                    if(existing_unit == ingredient.quantity_unit):
                        print('units match')
                        existing_item.ingredient_quantity = float(existing_quantity) + float(ingredient.ingredient_quantity)
                        existing_item.save()
                        created_item = True
                        break
                    else:
                        print('units dont match, try matching')
                        existing_parsed_unit_info = parse_unit(existing_unit)
                        incoming_parsed_unit_info = parse_unit(ingredient.quantity_unit)
                        if(not existing_parsed_unit_info[0] == 'not found' or not incoming_parsed_unit_info == 'not found'):
                            print('valid units')
                            multiplier = convert_units(incoming_parsed_unit_info[0], incoming_parsed_unit_info[1], existing_parsed_unit_info[0], existing_parsed_unit_info[1])
                            if not multiplier == 0: 
                                
                                existing_item.ingredient_quantity = float(existing_quantity) + (float(ingredient.ingredient_quantity) * multiplier)
                                existing_item.save()
                                created_item = True
                                break
                            else:
                                continue
                if(not created_item):
                    print('create new')
                    shopping_item = ShoppingListItem.objects.create(item_name=ingredient.ingredient_name, user = user,ingredient_quantity=ingredient.ingredient_quantity, 
                                                        quantity_unit=ingredient.quantity_unit)
                    shopping_item.save()

            else:
                print('create new')
                shopping_item = ShoppingListItem.objects.create(item_name=ingredient.ingredient_name, user = user,ingredient_quantity=ingredient.ingredient_quantity, 
                                                        quantity_unit=ingredient.quantity_unit)
                shopping_item.save()


    return Response("shopping list items successfully generated")




def parse_unit(unit_name):

    #weight
    weight = {
        'grams': ['g', 'grams'],
        'kilograms': ['kg', 'kilograms'],
        'pound': ['lb', 'pounds'], 
        'ouce': ['oz', 'ounce']
    }
    #spoons
    spoon = {
        'teaspoon': ['tsp', 'teaspoon'],
        'tablespoon':['tbsp', 'tablespoon'],
    }
    #volume
    volume = {
        'cup': ['cup'], 
        'liter': ['liter', 'l'], 
        'fluid_oz': ['fluid oz', 'fl oz', 'fluid ounce', 'fl ounce', 'fluid_oz'], 
        'ml': ['ml', 'milliliter'], 
        'gallon': ['gal', 'gallon'], 
    }

    parsed_unit = 'not found'
    for unit in weight:
        for str in weight[unit]:
            if(unit_name == str):
                parsed_unit = unit
                unit_type = 'weight'

    for unit in spoon:
        for str in spoon[unit]:
            if(unit_name == str):
                parsed_unit = unit
                unit_type = 'spoon'

    for unit in volume:
        for str in volume[unit]:
            if(unit_name == str):
                parsed_unit = unit
                unit_type = 'volume'


    return [parsed_unit, unit_type]


def convert_units(new_unit, new_unit_type,  database_unit, database_unit_type):
    if(new_unit_type == database_unit_type):
        weight_conversion = [['grams','kilograms', .001], ['grams','pound', 0.002], ['grams','ouce', 0.035],
                        ['kilograms','grams', 1000],['kilograms','pound', 2.205],['kilograms','ouce', 35.274],
                        ['pound','grams', 453.592],['pound','kilograms', 0.454],['pound','ouce', 16],
                        ['ouce','grams', 28.350],['ouce','kilograms', 0.028],['ouce','pound', 0.063]]
        spoon_conversion = [['teaspoon','tablespoon', .33], ['tablespoon','teaspoon', 3]]
        volume_conversion = [['cup','liter', .237], ['cup','fluid_oz', 8], ['cup','ml', 236.588],['cup','gallon', .063],
                            ['liter','cup', 4.227], ['liter','fluid_oz', 33.814], ['liter','ml', 1000],['liter','gallon', .264],
                            ['fluid_oz','cup', .125], ['fluid_oz','liter', .003], ['fluid_oz','ml', 29.574],['fluid_oz','gallon', .007],
                            ['ml','cup', .004], ['ml','liter', .001], ['ml','fluid_oz', .034],['ml','gallon', .0002],
                            ['gallon','cup', 16], ['gallon','liter', 3.785], ['gallon','fluid_oz', 128],['gallon','ml', 3785.41]]
        if(new_unit_type == 'weight'):
            for i in range(len(weight_conversion)):
                if(new_unit == weight_conversion[i][0] and database_unit == weight_conversion[i][1]):
                    return weight_conversion[i][2]
        if(new_unit_type == 'spoon'):
            for i in range(len(spoon_conversion)):
                if(new_unit == spoon_conversion[i][0] and database_unit == spoon_conversion[i][1]):
                    return spoon_conversion[i][2]
        if(new_unit_type == 'volume'):
            for i in range(len(volume_conversion)):
                if(new_unit == volume_conversion[i][0] and database_unit == volume_conversion[i][1]):
                    return volume_conversion[i][2]
    
    else:
        return 0