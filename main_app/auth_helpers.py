from django.contrib.auth.models import User
import jwt
from django.conf import settings



def validate_token(bearer_token, user: User):
    if not bearer_token:
        raise Exception("access denied..who are you?")
    token = bearer_token.split(' ')[1]  # remove Bearer
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    token_user_id = decoded['id']
    token_email = decoded['email']
    if user.id != token_user_id or user.email != token_email:
        raise Exception("access denied..who are you?")