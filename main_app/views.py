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

# Create your views here.

########### USER #############
def login_view(request):
    if request.method == 'POST':
        # try to log the user in
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user) # log the user in by creating a session
                    return redirect('/user/'+u)
                else:
                    print('The account has been disabled.')
                    return redirect('http://localhost:3000/login')
        else:
            print('The username and/or password is incorrect.')
            return redirect('http://localhost:3000/login')
    # else: # it was a GET request so send the empty login form
    #     form = AuthenticationForm()
    #     return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/cats')


# def signup_view(request):
#     if request.method == 'POST':
#         print('post info:', request.POST)
   
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             # return redirect('/user/'+str(user))
#             return redirect('http://localhost:3000/login')
#         else:
#             return HttpResponse('<h1>Try Again</h1>')
#     else:
#         form = UserCreationForm()
#             return render(request, 'signup.html', {'form': form})

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
