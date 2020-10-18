#from django.contrib.auth.models import User
from .models import Users, UsersVoiceTry, UsersFaceTry
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("username","email","password","face_1","face_2","voice")#,"is_staff","is_active","is_superuser","last_login","date_joined")
        read_only_fields = ("password")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {'password': {'write_only':True}}
    
    def create(self, validated_data):
        user = Users(
            email    = validated_data['email'],
            username = validated_data['username'],
            face_1   = validated_data['face_1'],
            face_2   = validated_data['face_2'],
            voice    = validated_data['voice'],
        )

        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class UsersVoiceTrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersVoiceTry
        fields = '__all__'

class UsersFaceTrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersFaceTry
        fields = '__all__'