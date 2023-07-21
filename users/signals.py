from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from .models import Profile, Location

@receiver(post_save, sender=User) # this is a decorator, it is a signal that gets fired after an object is saved
#user gets saved on db run the server

def create_user_profile(sender, instance, created, **kwargs): # this function is called whenever a user is created
    if created:
        Profile.objects.create(user=instance) # create a profile object with the user that was just created

@receiver(post_save, sender=Profile)
def create_profile_location(sender, instance, created, **kwargs):
    if created:
        profile_location = Location.objects.create()
        instance.location = profile_location
        instance.save()


@receiver(post_delete, sender=Profile)
def delete_profile_location(sender, instance, *args, **kwargs):
    if instance.location != None:
        instance.location.delete()
