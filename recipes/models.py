from django.db import models
import datetime
from django.utils import timezone 
from django.contrib import admin
from django.contrib.auth.models import User


# Create your models here.

class RecipeCategory(models.Model):
    category_name: models.CharField(max_length=50)
    def __str__(self):
        return self.category_name


class Recipe(models.Model):
    recipe_name: models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_category: models.ForeignKey(RecipeCategory, to_field='category_name', default='other')
    image = models.CharField(max_length=200)

    
    def __str__(self):
        return self.recipe_name + 'in category ' + self.recipe_category

class RecipeStep(models.Model):
    step_number: models.IntegerField()
    instructions: models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)