import requests

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.decorators import (
    permission_classes,
    authentication_classes,
    api_view
)
from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticated
)
from rest_framework.response import Response

from .serializers import UserSerializer
from .utils import get_db

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''registration for users'''

    data = request.data
    print(data)
    if not UserSerializer(data=data).is_valid():
        print(1)
        return Response(status=400)

    if len(User.objects.filter(username=data.get('username'))) > 0:
        print(2)
        return Response(status=400)

    user = User.objects.create_user(
        username = data.get('username'),
        password = data.get('password')
    )
    get_db().get_collection('roles').insert_one({
        "user_id": str(user.id),
        "role": "user"
    })
    
    token_request = requests.post('http://127.0.0.1:8000/api/access/', json={
        "username": data.get('username'),
        "password": data.get('password')
    })
    token_responce = token_request.json()

    return Response(data={
        "access": token_responce.get('access'),
        "refresh": token_responce.get('refresh')
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def auth(request):
    '''request for user's auth'''

    data = request.data
    print(data)
    if not UserSerializer(data=data).is_valid():
        print(1)
        return Response(status=400)

    user = authenticate(username=data.get('username'), password=data.get('password'))
    if user == None:
        print(2)
        return Response(status=400)

    token_request = requests.post('http://127.0.0.1:8000/api/access/', json={
        "username": data.get('username'),
        "password": data.get('password')
    })
    token_responce = token_request.json()

    role = get_db().get_collection('roles').find_one({"user_id": str(user.id)}).get('role')
    
    return Response(data={
        "access": token_responce.get('access'),
        "refresh": token_responce.get('refresh'),
        "role": role
    })

    