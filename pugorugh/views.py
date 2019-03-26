from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from . import models
from . import serializers
from . import permissions


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    model = get_user_model()
    serializer_class = serializers.UserSerializer


def convert_age(ages):
    """
    Converts age strings to nubmer lists
    """
    age_list = []
    for age in ages:
        if age == 'b':
            age_list.extend(list(range(0, 7)))
        elif age == 'y':
            age_list.extend(list(range(7, 23)))
        elif age == 'a':
            age_list.extend(list(range(23, 70)))
        elif age == 's':
            age_list.extend(list(range(70, 360)))
    return age_list


class RetrieveUpdateUserPrefView(generics.RetrieveUpdateAPIView):
    """
    Get or set user preferences
    """
    permission_classes = (permissions.UpdateOwnPreferences,
                          IsAuthenticated, )
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        """
        Get logged in users preferences
        """
        user = self.request.user
        return get_object_or_404(self.get_queryset(), user=user)


class RetrieveDogView(generics.RetrieveAPIView):
    """
    Dogs view by status and user preferences
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        """
        Filter query by status and user preferences
        """
        user = self.request.user
        status = self.kwargs.get('status')

        if status == 'liked':
            user_dogs = models.UserDog.objects.filter(
                user=user,
                status__icontains='l'
            ).values_list(
                'dog_id', flat=True
            )
            queryset = models.Dog.objects.filter(id__in=user_dogs)
        elif status == 'disliked':
            user_dogs = models.UserDog.objects.filter(
                user=user,
                status__icontains='d'
            ).values_list(
                'dog_id', flat=True
            )
            queryset = models.Dog.objects.filter(id__in=user_dogs)
        else:
            userpref = get_object_or_404(models.UserPref, user=user)
            userpref_ages = convert_age(userpref.age.split(','))
            user_dogs = models.UserDog.objects.filter(
                user_id__exact=user.pk
            ).values_list('dog_id', flat=True)

            queryset = models.Dog.objects.exclude(
                id__in=user_dogs
            ).filter(
                gender__in=userpref.gender.split(','),
                size__in=userpref.size.split(','),
                age__in=userpref_ages
            )
        return queryset

    def get_object(self):
        """
        return one dog object
        """
        pk = self.kwargs.get('pk')
        queryset = self.get_queryset().filter(
            pk__gt=pk
        ).order_by('pk')
        obj = queryset.first()
        return obj


class UpdateDogView(generics.UpdateAPIView):
    """
    Updates dog status for the user
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.DogSerializer

    def put(self, request, *args, **kwargs):
        """
        Updates userdog status
        """
        user = self.request.user
        status = self.kwargs.get('status')
        pk = self.kwargs.get('pk')

        dog = models.Dog.objects.get(pk=pk)
        user_dog = models.UserDog.objects.filter(user=user, dog_id=pk)

        if user_dog:
            if status == 'liked':
                user_dog.update(status='l')
            elif status == 'disliked':
                user_dog.update(status='d')
            else:
                user_dog.delete()
        else:
            models.UserDog.objects.create(
                status=status[0],
                dog_id=pk,
                user=user
            )
        serializer = serializers.DogSerializer(dog)
        return Response(data=serializer.data)


class DogProfileViewSet(viewsets.ModelViewSet):
    """
    Handled managing dogs
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()
    permission_classes = (permissions.UpdateOwnDog,
                          IsAuthenticated, )

    def perform_create(self, serializer):
        """
        Sets the creater of the dog to the logged in user
        """
        serializer.save(user=self.request.user)
