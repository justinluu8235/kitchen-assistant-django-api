from datetime import date, datetime, timedelta

from rest_framework.decorators import api_view

from recipes.serializers import RecipeSerializer
from  .serializers import MenuItemSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import MenuItem
from recipes.models import Recipe
from main_app.auth_helpers import validate_token

# order matters
DAY_NAMES = ("", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")

def get_date_from_iso(year, week_num, day_num):
    # Calculate the date of the first day of the ISO week
    jan_4th = date(year, 1, 4) # January 4th is always in the first ISO week
    jan_4th_day_num = jan_4th.weekday() # Get the day of the week (0-6, where Monday is 0)
    first_day_of_iso_week = jan_4th - timedelta(days=jan_4th_day_num - 1)

    # Calculate the date of the desired day within the ISO week
    delta = timedelta(weeks=week_num-1, days=day_num-1) # Subtract 1 from week_num and day_num to account for 0-based indexing
    date_from_iso = first_day_of_iso_week + delta

    return date_from_iso


@api_view(['GET'])
def menu_old_index(request, id):
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

@api_view(['GET'])
def menu_index(request, id):
    user = User.objects.get(pk=id)
    print(f'menu request == = {request}')
    try:
        validate_token(request.headers.get("Authorization"), user)
    except Exception as e:
        return Response(data={"error": "access denied..who are you?"}, status=400)

    # Get the date for the first day of the current week (Monday)
    # today = datetime.today()
    # monday = today - timedelta(days=today.weekday())
    # monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)

    # menu_list = MenuItem.objects.filter(user=user, cook_date__gte=monday.date()).order_by("cook_date")
    menu_list = MenuItem.objects.filter(user=user).order_by("cook_date")

    serializer = MenuItemSerializer(menu_list, many=True)
    # key will be the start of the week date.
    # val will be a dict with the week_end_date, day_of_week:[recipes]
    menu_dict = {}
    try:
        for i, menu_item in enumerate(menu_list):
            recipe = menu_item.recipe
            serializer.data[i]['recipe_name'] = recipe.recipe_name
            serializer.data[i]['image'] = str(recipe.image)

            cook_date = menu_item.cook_date
            year, week_num, day_of_week = cook_date.isocalendar()
            day = DAY_NAMES[day_of_week]
            first_date_of_week = str(get_date_from_iso(year, week_num, 0))
            last_date_of_week = str(get_date_from_iso(year, week_num, 6))
            if menu_dict.get(first_date_of_week):
                if menu_dict[first_date_of_week].get(day):
                    menu_dict[first_date_of_week][day].append(serializer.data[i])
                else:
                    menu_dict[first_date_of_week][day] = [serializer.data[i]]
            else:
                menu_dict[first_date_of_week] = {
                    "week_end_date": last_date_of_week,
                    f"{day}": [serializer.data[i]],
                }
    except Exception as e:
        print(f"Error building menu dict: {e}")
    return Response(menu_dict)


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

    # Get the date for the first day of the current week (Monday)
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)

    menu_list = MenuItem.objects.filter(user=user, cook_date__gte=monday.date()).order_by("cook_date")
    serializer = MenuItemSerializer(menu_list, many=True)
    # key will be the start of the week date.
    # val will be a dict with the week_end_date, day_of_week:[recipes]
    menu_dict = {}
    for i, menu_item in enumerate(menu_list):
        recipe = menu_item.recipe
        serializer.data[i]['recipe_name'] = recipe.recipe_name
        serializer.data[i]['image'] = str(recipe.image)

        cook_date = menu_item.cook_date
        year, week_num, day_of_week = cook_date.isocalendar()
        day = DAY_NAMES[day_of_week]
        first_date_of_week = str(date.fromisocalendar(year, week_num, 1))
        last_date_of_week = str(date.fromisocalendar(year, week_num, 7))
        if menu_dict.get(first_date_of_week):
            if menu_dict[first_date_of_week].get(day):
                menu_dict[first_date_of_week][day].append(serializer.data[i])
            else:
                menu_dict[first_date_of_week][day] = [serializer.data[i]]
        else:
            menu_dict[first_date_of_week] = {
                "week_end_date": last_date_of_week,
                f"{day}": [serializer.data[i]],
            }
    return Response(menu_dict)


