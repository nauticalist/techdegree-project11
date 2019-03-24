from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        fields = (
            'id',
            'username',
            'password'
        )
        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):
    """
    Serializer for the Dog Model
    """
    class Meta:
        fields = (
            'id',
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size'
        )
        model = models.Dog


class UserPrefSerializer(serializers.ModelSerializer):
    """
    Serializer for the User Preferences Model
    """
    class Meta:
        fields = (
            'user',
            'age',
            'gender',
            'size',
        )
        model = models.UserPref
        extra_kwargs = {
            'user': {'read_only': True}
        }


class UserDogSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserDog model
    """
    class Meta:
        fields = ('status', )
        model = models.UserDog