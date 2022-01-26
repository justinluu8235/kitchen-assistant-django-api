import requests

from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")
# query='fish'
# queryResultsQuantity = 5
# url = 'https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={API_KEY}&number={queryResultsQuantity}'.format(query=query, API_KEY=API_KEY, queryResultsQuantity=queryResultsQuantity )
# print(url)
# response = requests.get(url)
# print("API Response", response.json())
'''
API Response {'results': [
    {'id': 642929, 'title': 'Fish Congee', 'image': 'https://spoonacular.com/recipeImages/642929-312x231.jpg', 'imageType': 'jpg'}, 
    {'id': 4273, 'title': 'Fish Hunan Style', 'image': 'https://spoonacular.com/recipeImages/4273-312x231.jpg', 'imageType': 'jpg'}, 
    {'id': 642927, 'title': 'Fish Crocchette Appetizer', 'image': 'https://spoonacular.com/recipeImages/642927-312x231.jpg', 'imageType': 'jpg'}, 
    {'id': 642941, 'title': 'Fish Fillet In Creamy Coconut Curry', 'image': 'https://spoonacular.com/recipeImages/642941-312x231.jpg', 'imageType': 'jpg'}, 
    {'id': 642977, 'title': 'Fish Pie With Fresh and Smoked Salmon', 'image': 'https://spoonacular.com/recipeImages/642977-312x231.jpg', 'imageType': 'jpg'}]
    , 'offset': 0, 'number': 5, 'totalResults': 317}

'''
# apiRecipeId = 642929
# url = 'https://api.spoonacular.com/recipes/{apiRecipeId}/information?apiKey={API_KEY}&includeNutrition=false'
# url = url.format(apiRecipeId=apiRecipeId, API_KEY=API_KEY)
# response = requests.get(url)
# response = response.json()
# recipe_title = response['title']
# recipe_image = response['image']
# ingredientArr = list(map(parse_ingredients, response['extendedIngredients'] ))
# print(ingredientArr)


# def parse_ingredients(ingredient):
#     parsed_ingredient = {
#             'ingredient_name': ingredient['name'],
#             'ingredient_quant': ingredient["amount"],
#             'ingredient_unit': ingredient['unit']
#         }
#     return parsed_ingredient



'''
Fish Congee

https://spoonacular.com/recipeImages/642929-556x370.jpg

[{'id': 15015, 'aisle': 'Seafood', 'image': 'cod-fillet.jpg', 'consistency': 'solid', 'name': 'cod filet', 'nameClean': 'cod fillets', 'original': '1 1/2 pounds cod filet', 'originalString': '1 1/2 pounds cod filet', 'originalName': 'cod filet', 'amount': 1.5, 'unit': 'pounds', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 1.5, 'unitShort': 'lb', 'unitLong': 'pounds'}, 'metric': {'amount': 680.389, 'unitShort': 'g', 'unitLong': 'grams'}}}, 

{'id': 11216, 'aisle': 'Produce;Ethnic Foods;Spices and Seasonings', 'image': 'ginger.png', 'consistency': 'solid', 'name': 'ginger', 'nameClean': 'ginger', 'original': '1 piece ginger', 'originalString': '1 piece ginger', 'originalName': 'ginger', 'amount': 1.0, 'unit': 'piece', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 1.0, 'unitShort': '', 'unitLong': ''}, 'metric': {'amount': 1.0, 'unitShort': '', 'unitLong': ''}}}, 

{'id': 6176, 'aisle': 'Ethnic Foods', 'image': 'oyster-sauce.jpg', 'consistency': 'liquid', 'name': 'oyster sauce', 'nameClean': 'oyster sauce', 'original': '2 tablespoons oyster sauce', 'originalString': '2 tablespoons oyster sauce', 'originalName': 'oyster sauce', 'amount': 2.0, 'unit': 'tablespoons', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 2.0, 'unitShort': 'Tbsps', 'unitLong': 'Tbsps'}, 'metric': {'amount': 2.0, 'unitShort': 'Tbsps', 'unitLong': 'Tbsps'}}}, 

{'id': 20444, 'aisle': 'Pasta and Rice', 'image': 'uncooked-white-rice.png', 'consistency': 'solid', 'name': 'rice', 'nameClean': 'rice', 'original': '1.5 cups rice, washed', 'originalString': '1.5 cups rice, washed', 'originalName': 'rice, washed', 'amount': 1.5, 'unit': 'cups', 'meta': ['washed'], 'metaInformation': ['washed'], 'measures': {'us': {'amount': 1.5, 'unitShort': 'cups', 'unitLong': 'cups'}, 'metric': {'amount': 354.882, 'unitShort': 'ml', 'unitLong': 'milliliters'}}}, {'id': 43479, 'aisle': 'Alcoholic Beverages', 'image': 'sake.png', 'consistency': 'solid', 'name': 'rice wine', 'nameClean': 'shaoxing wine', 'original': '1 tablespoon Chinese rice wine', 'originalString': '1 tablespoon Chinese rice wine', 'originalName': 'Chinese rice wine', 'amount': 1.0, 'unit': 'tablespoon', 'meta': ['chinese'], 'metaInformation': ['chinese'], 'measures': {'us': {'amount': 1.0, 'unitShort': 'Tbsp', 'unitLong': 'Tbsp'}, 'metric': {'amount': 1.0, 'unitShort': 'Tbsp', 'unitLong': 'Tbsp'}}}, {'id': 2047, 'aisle': 'Spices and Seasonings', 'image': 'salt.jpg', 'consistency': 'solid', 'name': 'salt', 'nameClean': 'salt', 'original': 'pinch of salt', 'originalString': 'pinch of salt', 'originalName': 'pinch of salt', 'amount': 1.0, 'unit': 'pinch', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 1.0, 'unitShort': 'pinch', 'unitLong': 'pinch'}, 'metric': {'amount': 1.0, 'unitShort': 'pinch', 'unitLong': 'pinch'}}}, {'id': 4058, 'aisle': 'Ethnic Foods', 'image': 'sesame-oil.png', 'consistency': 'liquid', 'name': 'sesame oil', 'nameClean': 'sesame oil', 'original': '1 tablespoon sesame oil', 'originalString': '1 tablespoon sesame oil', 'originalName': 'sesame oil', 'amount': 1.0, 'unit': 'tablespoon', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 1.0, 'unitShort': 'Tbsp', 'unitLong': 'Tbsp'}, 'metric': {'amount': 1.0, 'unitShort': 'Tbsp', 'unitLong': 'Tbsp'}}}, {'id': 11677, 'aisle': 'Produce', 'image': 'shallots.jpg', 'consistency': 'solid', 'name': 'shallot', 'nameClean': 'shallot', 'original': 'some fried shallot', 'originalString': 'some fried shallot', 'originalName': 'some fried shallot', 'amount': 4.0, 'unit': 'servings', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 4.0, 'unitShort': 'servings', 'unitLong': 'servings'}, 'metric': {'amount': 4.0, 'unitShort': 'servings', 'unitLong': 'servings'}}}, {'id': 16124, 'aisle': 'Ethnic Foods;Condiments', 'image': 'soy-sauce.jpg', 'consistency': 'liquid', 'name': 'soya sauce', 'nameClean': 'soy sauce', 'original': '1 tablespoon soya sauce', 'originalString': '1 tablespoon soya sauce', 'originalName': 'soya sauce', 'amount': 1.0, 'unit': 'tablespoon', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 1.0, 'unitShort': 'Tbsp', 'unitLong': 'Tbsp'}, 'metric': {'amount': 1.0, 'unitShort': 'Tbsp', 'unitLong': 'Tbsp'}}}, {'id': 11291, 'aisle': 'Produce', 'image': 'spring-onions.jpg', 'consistency': 'solid', 'name': 'spring onions', 'nameClean': 'spring onions', 'original': 'some chopped spring onions, to garnish', 'originalString': 'some chopped spring onions, to garnish', 'originalName': 'some chopped spring onions, to garnish', 'amount': 4.0, 'unit': 'servings', 'meta': ['chopped'], 'metaInformation': ['chopped'], 'measures': {'us': {'amount': 4.0, 'unitShort': 'servings', 'unitLong': 'servings'}, 'metric': {'amount': 4.0, 'unitShort': 'servings', 'unitLong': 'servings'}}}, {'id': 14412, 'aisle': 'Beverages', 'image': 'water.png', 'consistency': 'liquid', 'name': 'water', 'nameClean': 'water', 'original': '2 liters of water (spare a bit more to adjust the consistency)', 'originalString': '2 liters of water (spare a bit more to adjust the consistency)', 'originalName': 'water (spare a bit more to adjust the consistency)', 'amount': 2.0, 'unit': 'liters', 'meta': ['(spare a bit more to adjust the consistency)'], 'metaInformation': ['(spare a bit more to adjust the consistency)'], 'measures': {'us': {'amount': 2.113, 'unitShort': 'qt', 'unitLong': 'quarts'}, 'metric': {'amount': 2.0, 'unitShort': 'l', 'unitLong': 'liters'}}}, {'id': 2032, 'aisle': 'Spices and Seasonings', 'image': 'white-pepper.png', 'consistency': 'solid', 'name': 'white pepper', 'nameClean': 'white pepper', 'original': '1/2 teaspoon white pepper', 'originalString': '1/2 teaspoon white pepper', 'originalName': 'white pepper', 'amount': 0.5, 'unit': 'teaspoon', 'meta': ['white'], 'metaInformation': ['white'], 'measures': {'us': {'amount': 0.5, 'unitShort': 'tsps', 'unitLong': 'teaspoons'}, 'metric': {'amount': 0.5, 'unitShort': 'tsps', 'unitLong': 'teaspoons'}}}]
'''


apiRecipeId = 642929
url = 'https://api.spoonacular.com/recipes/{apiRecipeId}/analyzedInstructions?apiKey={API_KEY}'
url = url.format(apiRecipeId=apiRecipeId, API_KEY=API_KEY)
response = requests.get(url)
response = response.json()
response = response[0]['steps']
print(response)


'''
[{'number': 1, 'step': 'In a big pot (a cocotte if you have one), put in the rice and water. Bring it to a boil.When it comes to a boiling point, give it a good stir. Put in some salt and the sliced ginger. Then, put the lid on. Turn the heat to low.Check and stir from time to time. It takes probably 20-30 minutes for the grains to start breaking. If you use Jasmine rice, it will be quicker. Long grain rice like basmati takes slightly longer.', 'ingredients': [{'id': 10220444, 'name': 'long grain rice', 'localizedName': 'long grain rice', 'image': 'rice-white-long-grain-or-basmatii-cooked.jpg'}, {'id': 10120444, 'name': 'jasmine rice', 'localizedName': 'jasmine rice', 'image': 'rice-jasmine-cooked.jpg'}, {'id': 11216, 'name': 'ginger', 'localizedName': 'ginger', 'image': 'ginger.png'}, {'id': 0, 'name': 'grains', 'localizedName': 'grains', 'image': ''}, {'id': 14412, 'name': 'water', 'localizedName': 'water', 'image': 'water.png'}, {'id': 20444, 'name': 'rice', 'localizedName': 'rice', 'image': 'uncooked-white-rice.png'}, {'id': 2047, 'name': 'salt', 'localizedName': 'salt', 'image': 'salt.jpg'}], 'equipment': [{'id': 404752, 'name': 'pot', 'localizedName': 'pot', 'image': 'stock-pot.jpg'}], 'length': {'number': 30, 'unit': 'minutes'}}, {'number': 2, 'step': 'Let it cook for about 1.5-2 hours. Remember to stir and check the consistency. If it becomes too thick, add some water. I usually tend not not make it too runny. The consistency that I always look for is like something like the consistency of pancake batter.Once it has been cooked under low heat for about 2 hours with desired consistency achieved, stir in the cod/haddock fillet that has been cut into cubes.', 'ingredients': [{'id': 15033, 'name': 'haddock', 'localizedName': 'haddock', 'image': 'catfish.jpg'}, {'id': 14412, 'name': 'water', 'localizedName': 'water', 'image': 'water.png'}, {'id': 15015, 'name': 'cod', 'localizedName': 'cod', 'image': 'cod-fillet.jpg'}], 'equipment': [], 'length': {'number': 240, 'unit': 'minutes'}}, {'number': 3, 'step': 'Put the lid back on to let the fish cooked for about 15 minutes.', 'ingredients': [{'id': 10115261, 'name': 'fish', 'localizedName': 'fish', 'image': 'fish-fillet.jpg'}], 'equipment': [], 'length': {'number': 15, 'unit': 'minutes'}}, {'number': 4, 'step': 'Serve congee in bowls, sprinkles with some spring onions, fried gingers and onions. You can adjust the seasoning by adding soya sauce if you wish (I always like this).', 'ingredients': [{'id': 11291, 'name': 'spring onions', 'localizedName': 'spring onions', 'image': 'spring-onions.jpg'}, {'id': 16124, 'name': 'soy sauce', 'localizedName': 'soy sauce', 'image': 'soy-sauce.jpg'}, {'id': 1042027, 'name': 'seasoning', 'localizedName': 'seasoning', 'image': 'seasoning.png'}, {'id': 93645, 'name': 'sprinkles', 'localizedName': 'sprinkles', 'image': 'colorful-sprinkles.jpg'}, {'id': 11282, 'name': 'onion', 'localizedName': 'onion', 'image': 'brown-onion.png'}], 'equipment': [{'id': 404783, 'name': 'bowl', 'localizedName': 'bowl', 'image': 'bowl.jpg'}]}, {'number': 5, 'step': 'Drizzle some sesame oil and a few dash of white pepper (to give a real kick to this dish!)', 'ingredients': [{'id': 2032, 'name': 'white pepper', 'localizedName': 'white pepper', 'image': 'white-pepper.png'}, {'id': 4058, 'name': 'sesame oil', 'localizedName': 'sesame oil', 'image': 'sesame-oil.png'}], 'equipment': []}]
'''