from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from pugorugh import models, serializers


class ViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test@domain.tld",
            password="testpass",
            first_name="test",
            last_name="User"
        )
        self.dog1 = models.Dog.objects.create(
            name='dogy1',
            breed='labrador',
            age='27',
            gender='m',
            size='l'
        )
        self.dog2 = models.Dog.objects.create(
            name='dogy_liked',
            gender='f',
            size='s'
        )
        self.dog3 = models.Dog.objects.create(
            name='dogy_disliked',
            gender='m',
            size='xl'
        )
        self.likeduserdog = models.UserDog.objects.create(
            user=self.user,
            dog=self.dog2,
            status="l"
        )
        self.dislikeduserdog = models.UserDog.objects.create(
            user=self.user,
            dog=self.dog3,
            status="d"
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_user_preferences(self):
        """
        Test page loads logged in users data
        """
        user_pref = models.UserPref.objects.get(user=self.user)
        resp = self.client.get(reverse('pugorugh:user-preferences'))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['age'], user_pref.age)
        self.assertEqual(resp.data['gender'], user_pref.gender)
        self.assertEqual(resp.data['size'], user_pref.size)
        self.assertEqual(resp.data['user'], user_pref.user.id)
    
    def test_update_user_preferences(self):
        """
        Test updating user preferences
        """
        payload = {'age': 'b,a', 'size': 'm,l'}
        resp = self.client.patch(reverse('pugorugh:user-preferences'), payload)

        user_pref = models.UserPref.objects.get(user=self.user)
        self.assertEqual(user_pref.age, payload['age'])
        self.assertEqual(user_pref.size, payload['size'])
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retrieve_undecided_dogs(self):
        """
        Tests for undecided dogs list
        """
        resp = self.client.get(reverse('pugorugh:next-dog',
            kwargs={'pk': '-1', 'status': 'undecided'}
        ))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('name'), self.dog1.name)
        self.assertNotEqual(resp.data.get('name'), self.dog2.name)
    
    def test_retrieve_liked_dogs(self):
        """
        Tests for liked dogs list
        """
        resp = self.client.get(reverse('pugorugh:next-dog',
            kwargs={'pk': '-1', 'status': 'liked'}
        ))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('name'), self.dog2.name)
        self.assertNotEqual(resp.data.get('name'), self.dog1.name)

    def test_retrieve_disliked_dogs(self):
        """
        Tests for disliked dogs
        """
        resp = self.client.get(reverse('pugorugh:next-dog',
            kwargs={'pk': '-1', 'status': 'disliked'}))
        self.assertEqual(resp.status_code,status.HTTP_200_OK)
        self.assertEqual(resp.data.get('name'), self.dog3.name)
    
    def test_update_dog_status_as_liked(self):
        """
        Test updating a disliked dog status as liked throug api
        """
        payload = {'status': 'liked', 'pk': self.dog3.id}
        resp = self.client.put(reverse('pugorugh:update-dog',
            kwargs=payload
        ))
        self.dislikeduserdog.refresh_from_db()
        self.assertEqual(self.dislikeduserdog.status, 'l')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_dog_status_as_disliked(self):
        """
        Test updating a liked dog status as disliked throug api
        """
        payload = {'status': 'disliked', 'pk': self.dog2.id}
        resp = self.client.put(reverse('pugorugh:update-dog',
            kwargs=payload
        ))
        self.likeduserdog.refresh_from_db()
        self.assertEqual(self.likeduserdog.status, 'd')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_dog_status_as_undecided(self):
        """
        Test updating a liked dog status as disliked throug api
        """
        payload = {'status': 'undecided', 'pk': self.dog3.id}
        resp = self.client.put(reverse('pugorugh:update-dog',
            kwargs=payload
        ))
        self.assertFalse(models.UserDog.objects.filter(
            dog_id__exact=self.dog3.id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_update_undecided_dog_as_liked(self):
        """
        Test creating a new liked dog
        """
        payload = {'status': 'liked', 'pk': self.dog1.id}
        resp = self.client.put(reverse('pugorugh:update-dog',
            kwargs=payload
        ))
        new_user_like = models.UserDog.objects.get(
            user=self.user, dog=self.dog1,
        )
        
        self.assertTrue(new_user_like.status, 'l')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)