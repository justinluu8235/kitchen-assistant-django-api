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
from .serializers import UserSerializer, UserFriendSerializer
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .models import UserFriend
from knox.models import AuthToken

# Create your views here.




########### USER #############

@api_view(['GET'])
def get_name(request, id):
    user_id = id
    user = User.objects.get(id=user_id)
    username = user.username
    return Response(username)


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
                    
                    token=jwt.encode({'id': user.id, 'username': user.username, 'email': user.email, 'password': user.password,
                            'exp': datetime.now() + timedelta(hours=9)}, 
                            settings.SECRET_KEY, algorithm='HS256')
                    print('token', token)
                    print('exp', datetime.now() + timedelta(hours=5))
                    user_info = {
                        'userData':
                        {
                        'username': user.username, 
                        'email': user.email,
                        'id': user.id, 
                        },
                        'token': 'Bearer ' + str(token),
                        'success': True
                    }
                    print(user_info)
                    data = json.dumps(user_info)
                    # serializer = UserSerializer(user_token)
                    return Response(data)
                # else:
                #     print('The account has been disabled.')
                #     return redirect('http://localhost:3000/login')
  

@api_view(['GET'])
def logout_view(request):
    print('logout request', request)
    logout(request)
    return Response('logged out')

@api_view(['POST'])
def signup_view(request):
    if(request.method == 'POST'):
        print("data incoming: ", request.data)
        sign_up_data = request.data
        dict = {'username': sign_up_data['email'], 'password1': sign_up_data['password'], 'password2': sign_up_data['password'], 'email': sign_up_data['email']}
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


@api_view(['GET'])
def userfriend_index(request, id):
    user_id = id
    
    user = User.objects.get(pk=id)

    #find current friends
    friend_list = UserFriend.objects.all().filter(user=user, currently_friends=True)

    #friend requests sent 
    request_pending_list = UserFriend.objects.all().filter(user=user, currently_friends=False, request_pending=True)
    
    #friend request received 
    request_received_list = UserFriend.objects.all().filter(friend_id=user_id, currently_friends=False, request_pending=True)
    
    
    friend_list_serializer = UserFriendSerializer(friend_list, many=True)
    request_pending_list_serializer = UserFriendSerializer(request_pending_list, many=True)
    request_received_list_serializer = UserFriendSerializer(request_received_list, many=True)
    print('receive', request_received_list_serializer)
    received_list = list(map(add_username, request_received_list_serializer.data))
    

    obj={
        'friend_list': friend_list_serializer.data,
        'request_pending_list' : request_pending_list_serializer.data,
        'request_received_list' : received_list,
    }
    print('response obj', obj)
    return Response(obj)

def add_username(request) :
    username = User.objects.get(pk=request['user']).username
    request['username'] = username
    return request



@api_view(['POST'])
def userfriend_search(request):
    search_username = request.data['search_username']
    user_id = request.data['user_id']

    user = User.objects.get(pk=user_id)
    print('user' , user)

    friend_user = User.objects.all().filter(username=search_username)
    print('user found', friend_user)
    if(not len(friend_user) == 0):
        print('friend name', friend_user[0].username)
        user_friend = UserFriend.objects.get_or_create(user=user, friend_name=friend_user[0].username, 
                                                friend_id=friend_user[0].id)

        print('user_friend obj', user_friend)



        user_friend_serializer = UserFriendSerializer(user_friend[0], many = False)
        obj = {
            'friend_status': user_friend_serializer.data
        }
    else:
        obj={
            'friend_status': 404
        }
    print('response obj', obj)
    return Response(obj)


@api_view(['POST'])
def userfriend_add(request):
    friend_username = request.data['friend_username']
    user_id = request.data['user_id']

    user = User.objects.get(pk=user_id)
    print('user' , user)

    friend_user = User.objects.all().filter(username=friend_username)
    print('user found', friend_user)
    if(not len(friend_user) == 0):
        print('friend name', friend_user[0].username)
        user_friend = UserFriend.objects.get_or_create(user=user, friend_name=friend_user[0].username, 
                                                friend_id=friend_user[0].id)
        user_friend[0].request_pending=True
        user_friend[0].save()
        print('user_friend obj', user_friend)



        user_friend_serializer = UserFriendSerializer(user_friend[0], many = False)
        obj = {
            'friend_status': user_friend_serializer.data
        }
    else:
        obj={
            'friend_status': 404
        }
    print('response obj', obj)
    return Response(obj)


@api_view(['POST'])
def userfriend_accept(request):
    requester_id = request.data['requester_id']
    receiver_name = request.data['receiver_name']

    requestor = User.objects.get(pk=requester_id)
    receiver = User.objects.get(username=receiver_name)

    user_friend = UserFriend.objects.get(user=requestor, friend_name=receiver_name)
    user_friend.currently_friends = True
    user_friend.request_pending = False
    user_friend.save()

    user_friend = UserFriend.objects.get_or_create(user=receiver, friend_name=requestor.username, 
                                                friend_id=requester_id )
    user_friend[0].currently_friends=True
    user_friend[0].equest_pending=False                                            
    user_friend[0].save()
    user_friend_serializer = UserFriendSerializer(user_friend[0])
    obj={
        'friend_status': user_friend_serializer.data
        }


    print('response obj', obj)
    return Response(obj)


@api_view(['POST'])
def userfriend_unfriend(request):
    friend_id = request.data['friend_id']
    user_id = request.data['user_id']

    friend = User.objects.get(pk=friend_id)
    user = User.objects.get(pk=user_id)
    print('friend', friend)
    print('user', user)

    user_friend1 = UserFriend.objects.get(user=user, friend_id=friend_id)
    user_friend2 = UserFriend.objects.get(user=friend, friend_id=user_id)
    user_friend1.delete()
    user_friend2.delete()

    return Response("Unfriended")



