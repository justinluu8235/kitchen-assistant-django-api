from django.contrib.auth.models import User
import jwt
from django.conf import settings

from main_app.models import UserFriend


def validate_token(bearer_token, user: User, friend_access=False):
    if not bearer_token:
        raise Exception("access denied..who are you?")
    token = bearer_token.split(' ')[1]  # remove Bearer
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    token_user_id = decoded['id']
    token_email = decoded['email']
    has_access = False
    # if not okay for friend to access, the token needs to match the user
    if not friend_access:
        if user.id == token_user_id and user.email == token_email:
            has_access = True
    # as long as they are friends
    else:
        has_access = UserFriend.objects.filter(user=user, friend_id=token_user_id).exists()
        if user.id == token_user_id and user.email == token_email:
            has_access = True

    if not has_access:
        raise Exception("access denied..who are you?")

