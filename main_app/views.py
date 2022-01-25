from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
import json
from django.http import QueryDict
from .serializers import UserSerializer
import jwt
from datetime import datetime, timedelta
from django.conf import settings

# Create your views here.

########### USER #############
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        # try to log the user in
        login_data = request.data
        print("Login data", login_data)
        dict = {'username': login_data['username'], 'password': login_data['password']}
        query_dict = QueryDict('', mutable=True)
        query_dict.update(dict)
        form = AuthenticationForm(request,query_dict)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user) # log the user in by creating a session
                    
                    token=jwt.encode({'username': user.username, 'email': user.email, 'password': user.password,
                            'exp': datetime.now() + timedelta(hours=24)}, 
                            settings.SECRET_KEY, algorithm='HS256')
                    user_token = {
                        'username': user.username, 
                        'email': user.email,
                        'id': user.id, 
                        'token': 'Bearer ' + str(token)
                    }
                    print(user_token)
                    serializer = UserSerializer(user_token)
                    return Response(serializer.data)
                # else:
                #     print('The account has been disabled.')
                #     return redirect('http://localhost:3000/login')
  


def logout_view(request):
    logout(request)
    return redirect('/cats')

@api_view(['POST'])
def signup_view(request):
    if(request.method == 'POST'):
        print("data incoming: ", request.data)
        sign_up_data = request.data
        dict = {'username': sign_up_data['name'], 'password1': sign_up_data['password'], 'password2': sign_up_data['password'], 'email': sign_up_data['email']}
        query_dict = QueryDict('', mutable=True)
        query_dict.update(dict)
        form = UserCreationForm(query_dict)
        print("Form Valid?", form.is_valid())
        if form.is_valid():
            user = form.save()
            user.email = sign_up_data['email']
            user.save()
            print("User created", user)
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        return Response("try again")


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username,'cats': cats})
