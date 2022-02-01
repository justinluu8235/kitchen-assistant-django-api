# Kitchen-Assistant v2.0 Backend API

The original kitchen assistant was built on the Expres/EJS stack, and was a website allowing users to efficiently manage logistics in their kitchen. This updated version is built with Django for its backend, React for frontend, and provides additional functionality. This API is to support the react frontend for this application.

For a full overview, see the <a href="https://github.com/justinluu8235/kitchen-assistant-frontend">Kitchen Assistant v2 Frontend Repo</a>

Helpful links:
[Kitchen-Assistant v2.0 via Heroku](https://kitchen-assistantv2-frontend.herokuapp.com/)

[Kitchen-Assistant Github Repository (Frontend)](https://github.com/justinluu8235/kitchen-assistant-frontend)

[Kitchen-Assistant Github Repository (Backend)](https://github.com/justinluu8235/kitchen-assistant-django-api)

[Oriignal v1 Kitchen-Assistant EJS-Express Github Repository](https://github.com/justinluu8235/kitchen-assistant)




## Give it a Try
* <a href="https://kitchen-assistantv2-frontend.herokuapp.com/">Go to the live site here</a>

* Follow these installation instructions
    * clone the repo and run it
    * run pip3 install -r requirements.txt
    * set up a .env with the following:
        -  FRONTEND_URL for frontend connection (can also clone our <a href="https://github.com/justinluu8235/kitchen-assistant-frontend">frontend repo</a>)
        - API_KEY for spoonacular. Can be obtained on their website for free
        - CLOUDINARY_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET that can be obtained from creating a free cloudinary account on their website
    * run npm start





## Spoonacular API
Searching recipes results in fetches from the spoonacular API with their instructions and steps stored in different routes. Data is then organized and sent for display

```python
@api_view(['get'])
def search_recipe_view(request, id):
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
    data=json.dumps(obj)
    return Response(data)
```





## Cloudinary Image Upload
Cloudinary-Python configuration is used for image upload for recipes. The Recipes model has an image field and settings are configured to upload images and fetch a cloudinary URL when recipes are created and edited.

```python
#recipes.models

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100, default='N/A')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_category = models.ForeignKey(RecipeCategory, on_delete=models.SET_NULL,  
                                            null=True)
    image = models.ImageField(_("Image"),max_length=200,  upload_to=upload_to, blank=True, null=True)
```
```python
#settings.py

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```





## Recipe Generation
Below is an example of recipe creation. The organization between the associations of the user, recipe category, instructions, and ingredients are important to maintaining the application.

```python
    # get user
    user = User.objects.get(pk=user_id)
    # get or create recipe category
    recipe_category = RecipeCategory.objects.get_or_create(category_name=recipe_category)
    recipe_category[0].user = user
    recipe_category[0].save()
    # create recipe
    new_recipe = Recipe.objects.create(recipe_name=recipe_name, user = user, recipe_category=recipe_category[0], image=recipe_image)
    new_recipe.save()
    # loop through instructions to create 
    for instructions in instructions_list:
        recipe_step = new_recipe.recipestep_set.create(step_number=instructions['step_number'], 
                        instructions=instructions['instructions'], image=None, recipe=new_recipe)
        recipe_step.save()
     # loop through instructions to create 
    for ingredients in ingredients_list:
        #ingredient info is parsed before being stored in the database
        parsed_ingredient_name = ingredients['ingredient_name'].lower().strip()
        parsed_quantity_unit = ingredients['quantity_unit'].lower().strip()
        if(len(parsed_quantity_unit) > 1 and parsed_quantity_unit[-1] == 's' ):
            parsed_quantity_unit = parsed_quantity_unit[:-1]
        ingredient = new_recipe.ingredient_set.create(ingredient_name=parsed_ingredient_name, 
                        ingredient_quantity=str(round(float(ingredients['ingredient_quantity']),2)), quantity_unit=parsed_quantity_unit, recipe=new_recipe)
        ingredient.save()
```






## Unit Conversion
One added feature is that when generating shopping list items, the goal is to have the same item names to not duplicate as shopping items, even though recipe notes different units. This logic is reviewed in the backend before generating shopping list items.


For common units, we first try to relate them 

```python
def parse_unit(unit_name):
    print(unit_name)

    #weight
    weight = {
        'grams': ['g', 'gram'],
        'kilograms': ['kg', 'kilogram'],
        'pound': ['lb', 'pound'], 
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
```

Find a multiplier between the input unit and the existing shopping list item unit
```python
weight_conversion = [['grams','kilograms', .001], ['grams','pound', 0.002], ['grams','ouce', 0.035],
                        ['kilograms','grams', 1000],['kilograms','pound', 2.205],['kilograms','ouce', 35.274],
                        ['pound','grams', 453.592],['pound','kilograms', 0.454],['pound','ouce', 16],
                        ['ouce','grams', 28.350],['ouce','kilograms', 0.028],['ouce','pound', 0.063]]
```

Then we apply a multiplier to the quantity and add it to an existing shopping list item
```python
if not multiplier == 0: 
                                print('multiplier', multiplier)
                                existing_item.ingredient_quantity = float(existing_quantity) + (float(ingredient.ingredient_quantity) * multiplier)
                                existing_item.save()
                                created_item = True

```







### RESTful Routing

The following table illustrates the API routes that are used by the frontend to interact with third-party APIs and the database.

 Verb | URL | Description
 ----------- | ----------- | -----------
 POST | /login | Logs in a user, returning a jwtToken
 GET | /logout |  Logs out user
 POST | /signup | Creates an user account
 GET | /name/:id | Gets the username of a user
 GET | /userFriends/:id |  Returns a parsed list of a user's friends, pending friend requests, and friend requsts sent 
 POST | /userFriends/search | Based on a search for another username, return friend status with that user
 POST | /userFriends/add |  Sends a friend request to another user
 POST | /userFriends/accept | Accept a friend request from a user
 POST | /userFriends/delete | Remove a user as a friend
 GET | /menu/:id | Returns all the menu items from a user organized by date
 POST | /menu/new | Creates a menu item based on recipe and the person requesting
 DELETE | /menu/delete/:id | Delete a menu item
 GET | /recipes/:id |  Get all the recipes associated with a user
 POST | /recipes/new |  Part 1 of recipe creation - using multiparser to recieve image file and initiate a recipe
 POST | /recipes/new-2 |  Part 2 of recipe creation - take in remainder recipe information to update the recipe
 GET | /recipes/view/:id |  Send a recipe's data, as well as its instructions and ingredients associated with it
 POST | /recipes/edit/:id |  Update all the recipe information except the image 
 POST | /recipes/edit-2 | Update recipe image
 DELETE | /recipes/delete/:id | Delete recipe
 POST | /recipes/searchRecipes |  Fetch Spoonacular API, parse data, and return recipe information
 GET | /recipes/searchRecipes/:id| Takes in recipe information and creates a recipe
 POST | /recipes/searchRecipes/new |  Search for a recipe on spoonacular API
 POST | /shoppinglist/newPantryItem |  Create a pantry item
 POST | /shoppinglist/new |  Create a new shopping list item
 GET | /shoppinglist/pantry/:id |  Returns a list of pantry items organized by category
 GET | /shoppinglist/:id |  Returns a list of shopping list items
 DELETE | /shoppinglist/pantry/delete/:id |  Delete pantry item
 DELETE | /shoppinglist/delete/:id |  Delete shopping list item
 POST | /shoppinglist/pantry/edit/:id | Update whether the pantry item is in_stock
 POST | /shoppinglist/generate |  Generate a shopping list based on a recipe. converts popular unit for ingredients to avoid unneccessary duplicate line items
