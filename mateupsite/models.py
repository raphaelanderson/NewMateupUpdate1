from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User


class Attribute(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField(default=1) # Relevance of the attr. Will allow for more accurate (weighted) matches to be implemented in the future
    enabled = models.BooleanField(default=False)
    description = models.TextField(max_length=800, blank=True)

    def __str__(self):
        return self.name


# Custom profile model that extends Django's User with a MateUp user profile information, based on:
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=True)
    address = models.TextField(max_length=500, blank=True)
    attributes = models.ManyToManyField('Attribute', blank=True)

    @property
    def name(self):
        return self.user.get_full_name()

    def __str__(self):
        return '{} ({})'.format(self.name, self.user.username)

#Basically we are hooking the create_user_profile and save_user_profile methods to the User model, whenever a save event occurs.
@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()