from django.db import models
from django.contrib.auth.models import User

class UserFriend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend_name = models.CharField(max_length=100)
    friend_id = models.IntegerField()
    currently_friends = models.BooleanField(default=False)
    request_pending = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + ' and ' + str(self.friend_name) + 'currently friends?' + str(self.currently_friends) + ', request pending?' + str(self.request_pending)
