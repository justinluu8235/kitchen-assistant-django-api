from django.db import models
import datetime
from django.utils import timezone 
from django.contrib.auth.models import User

# Create your models here.
class MenuItem(models.Model):
    cook_date = models.DateField(auto_now=False, auto_now_add=False)
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requester_username = models.CharField(max_length=100)