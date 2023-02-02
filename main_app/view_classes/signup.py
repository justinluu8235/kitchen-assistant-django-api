from django.contrib.auth.forms import UserCreationForm
from django.http import QueryDict
from rest_framework.response import Response
from django.contrib.auth import login
from main_app.serializers import UserSerializer


class SignupView:
    def sign_up(self, request):
        sign_up_data = request.data
        dict = {'username': sign_up_data['email'], 'password1': sign_up_data['password'],
                'password2': sign_up_data['password'], 'email': sign_up_data['email']}
        query_dict = QueryDict('', mutable=True)
        query_dict.update(dict)
        form = UserCreationForm(query_dict)
        print("Form Valid?", form.is_valid())
        if form.is_valid():
            try:
                user = form.save()
                user.email = sign_up_data['email']
                user.save()
                print("User created", user)
                serializer = UserSerializer(user)
            except Exception as e:
                print(f'error creating or saving user {e}')

            try:
                login(request, user)
            except Exception as e:
                print(f'Error logging in user: {e}')

            return Response(serializer.data)
        else:
            print(form.errors)
            # hacky way of cleaning username texts to email
            if 'username' in form.errors:
                error_msg = form.errors.get('username')
                if len(error_msg) > 0 and type(error_msg[0]) == str:
                    error_msg[0] = error_msg[0].replace('username', 'email')
                form.errors.pop('username', None)
                form.errors['email'] = error_msg
            cleaned_msg = ""
            for error in form.errors.keys():
                msg_arr = form.errors[error]
                if len(msg_arr) > 0:
                    for msg in msg_arr:
                        cleaned_msg += f"{msg} \n"

            return Response({"errors": cleaned_msg})
