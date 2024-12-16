from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from .models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework import serializers
from django.contrib.auth import get_user_model

User  = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class ShipmentSerializer(serializers.ModelSerializer):

    customer_data = serializers.ReadOnlyField()
    driver_data = serializers.ReadOnlyField()
    class Meta:
        model = Shipment
        fields = '__all__'



        
class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = "__all__"




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
