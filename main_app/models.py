from django.db import models
from django.contrib.auth.models import User

class UserFriend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend_name = models.CharField(max_length=100)
    friend_id = models.IntegerField()

    def __str__(self):
        return self.friend_name 