from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from user_app import models
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def logout_view(request):
    
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    

@api_view(['POST'])
def registration_view(request):  
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            user = serializer.save()
            data['message'] = "Registration Successfully!"
            data['username'] = user.username
            data['email'] = user.email
            refresh = RefreshToken.for_user(user)
             
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
             
            # data['token'] = Token.objects.get(user=user).key
        else:
            data = serializer.errors
        
        return Response(data)
