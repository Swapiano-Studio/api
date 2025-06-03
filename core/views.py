from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from django.contrib.auth.hashers import make_password

# Create your views here.

@api_view(['POST'])
def register_user(request):
    data = request.data
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return Response({'error': f'{field} is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if CustomUser.objects.filter(username=data['username']).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    if CustomUser.objects.filter(email=data['email']).exists():
        return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = CustomUser.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            city=data.get('city', ''),
            state=data.get('state', ''),
            address=data.get('address', ''),
            phone_number=data.get('phone_number', ''),
        )
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_biodata(request):
    user = request.user
    data = request.data
    # Update user fields if present in request data
    for field in ['first_name', 'last_name', 'city', 'state', 'address', 'phone_number', 'email']:
        if field in data:
            setattr(user, field, data[field])
    user.save()
    return Response({'message': 'Biodata updated successfully.'}, status=status.HTTP_200_OK)
