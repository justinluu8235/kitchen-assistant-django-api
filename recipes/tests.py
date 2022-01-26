from django.test import TestCase
from .models import Recipe, RecipeCategory
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
# Create your tests here.


#helper for test
def create_recipe_category(cat_name, user ):
    return RecipeCategory.objects.create(category_name=cat_name, user=user)

def create_user(username, password):
    return User.objects.create(username=username, password=password)

def create_recipe(recipe_name, user, recipe_category, image):
    return Recipe.objects.create(recipe_name=recipe_name, user=user, 
                                    recipe_category=recipe_category, image=image)

class RecipeCategoryModelTests(TestCase):
    def test_create_recipe_category(self):
        user = create_user(username='jack', password='SEI102599')
        recipe_cat = create_recipe_category("fish", user)
        self.assertIs(recipe_cat.user.username, 'jack')
        self.assertIs(recipe_cat.category_name, 'fish')
    
    def test_create_recipe_without_image(self):
        user = create_user(username='jack', password='SEI102599')
        recipe_cat = create_recipe_category("other", user)
        recipe = create_recipe("pie", user, None, None)
        self.assertIs(recipe.image, None)

    def test_get_category_name_from_recipe(self):
        user = create_user(username='jack', password='SEI102599')
        recipe_cat = create_recipe_category("other", user)
        recipe = create_recipe("pie", user, recipe_cat, None)
        self.assertIs(recipe.recipe_category.category_name, "other")

    def test_create_recipe_without_recipe_category(self):
        user = create_user(username='jack', password='SEI102599')
        # recipe_cat = create_recipe_category("other", user)
        recipe = create_recipe("pie", user, None, None)
        self.assertIs(recipe.recipe_category, None)


class RecipeIndexViewTests(TestCase):
    
    def test_get_recipes_by_users(self):
        user = create_user(username='jack', password='SEI102599')
        recipe_cat = create_recipe_category("fish", user)
        recipe = create_recipe("pie", user, recipe_cat, None)
        c = Client()
    
        c.login(username='jack', password='SEI102599')
        response = c.get(reverse('recipes:index'), follow=True)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        


        