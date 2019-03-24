from django.contrib.auth import get_user_model
from django.test import TestCase

from pugorugh import models

class ModelTests(TestCase):

    def setUp(self):
        """
        Create a sample data for tests
        """
        self.test_user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass",
            first_name="Test",
            last_name="User"
        )
        self.dog = models.Dog.objects.create(
            name='dogy',
            gender='m',
            size='l'
        )
    
    def test_dog_str(self):
        """
        Test dog model for string representation
        """
        self.assertEqual(str(self.dog), self.dog.name)

    def test_userdog_str(self):
        """
        Test userdog model for string representation
        """
        userdog = models.UserDog.objects.create(
            user=self.test_user,
            dog=self.dog,
            status='l'
        )
        
        self.assertIn(self.dog.name, str(userdog))
        self.assertIn(self.test_user.first_name, str(userdog))

    def test_userpref_str(self):
        """
        Test userpref created when user created
        and model string representation
        """
        userpref = models.UserPref.objects.get(
            user=self.test_user
        )

        self.assertIn(self.test_user.username, str(userpref))
