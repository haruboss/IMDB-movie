from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        
        if password != confirm_password:
            raise serializers.ValidationError({'error': "Password and confirm password should be same."})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': "Email Already exists."})
        
        user = User(email=self.validated_data['email'], username=self.validated_data['username'])
        user.set_password(password)
        
        
        user.save()
        return user
            