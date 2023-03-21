from django.db import models
import datetime
from django.utils import timezone 
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _




# Create your models here.

def upload_to(instance, filename):
    return 'recipes/{filename}'.format(filename=filename)

class RecipeCategory(models.Model):
    category_name = models.CharField(max_length=50, default="other")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'category_name'], name='unique_user_category_name')
        ]


    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        self.category_name = self.category_name.lower()
        super(RecipeCategory, self).save(*args, **kwargs)


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100, default='N/A')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(RecipeCategory, related_name='recipes', null=True)
    image = models.ImageField(_("Image"),max_length=300,  upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return f"Recipe({self.pk}: {self.recipe_name})"


class RecipeStep(models.Model):
    step_number = models.IntegerField(default=1)
    instructions = models.CharField(max_length=1000, default='N/A')
    image = models.CharField(max_length=200, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=100, default='N/A')
    ingredient_quantity = models.CharField(max_length=50, default='N/A')
    quantity_unit = models.CharField(max_length=50, default='N/A')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
