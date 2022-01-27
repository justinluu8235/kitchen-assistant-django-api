from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PantryCategory(models.Model):
    category_name= models.CharField(max_length=50, unique=True, default="other")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.category_name

class PantryItem(models.Model):
    item_name =  models.CharField(max_length=50)
    in_stock = models.BooleanField(default=False)
    pantry_category = models.ForeignKey(PantryCategory, on_delete=models.SET_DEFAULT,  
                                            to_field ='category_name', default="other")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name


class ShoppingListItem(models.Model):
    item_name =  models.CharField(max_length=50)
    ingredient_quantity = models.CharField(max_length=50, default='N/A')
    quantity_unit = models.CharField(max_length=50, default='N/A')
    user = models.ForeignKey(User, on_delete=models.CASCADE)