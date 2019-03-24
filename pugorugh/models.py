from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


GENDER = [
    ('m', 'male'),
    ('f', 'female'),
    ('u', 'unknown')
]

STATUS = [
    ('l', 'liked'),
    ('d', 'disliked')
]

AGE = [
    ('b', 'baby'),
    ('y', 'young'),
    ('a', 'adult'),
    ('s', 'senior')
]

GENDER = [
    ('m', 'male'),
    ('f', 'female')
]

SIZE = [
    ('s', 'small'),
    ('m', 'medium'),
    ('l', 'large'),
    ('xl', 'extra large')
]


class Dog(models.Model):
    """
    Dog object
    """
    name = models.CharField(max_length=100)
    image_filename = models.CharField(max_length=100, blank=True)
    breed = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    size = models.CharField(max_length=2, choices=SIZE)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    """
    Users related dogs object
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS)

    class Meta:
        unique_together = ['user', 'dog']

    def __str__(self):
        return "{} {} - {}".format(self.user.first_name,
                                   self.user.last_name,
                                   self.dog.name)


class UserPref(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=100, default='b,y,a,s')
    gender = models.CharField(max_length=100, default='m,f')
    size = models.CharField(max_length=100, default='s,m,l,xl')

    def __str__(self):
        return "{}'s preferences'".format(self.user.username)


@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """
    Create default user preferences when user instance created
    """
    if created:
        UserPref.objects.create(user=instance)