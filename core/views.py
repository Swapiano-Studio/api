from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .mongo_models import CustomUserDoc
from django.contrib.auth.hashers import make_password

# Create your views here.

@api_view(['POST'])
def register_user(request):
    data = request.data
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return Response({'error': f'{field} is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if CustomUserDoc.objects(username=data['username']).first():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    if CustomUserDoc.objects(email=data['email']).first():
        return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = CustomUserDoc(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password']),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            city=data.get('city', ''),
            state=data.get('state', ''),
            address=data.get('address', ''),
            phone_number=data.get('phone_number', ''),
        )
        user.save()
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
