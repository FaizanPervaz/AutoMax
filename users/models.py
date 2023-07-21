from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USStateField,USZipCodeField
from .utils import user_directory_path
# Create your models here.

class Location(models.Model):
    address_1 = models.CharField(max_length=128, blank=True)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=100)
    state = USStateField(default='NY')
    zipcode = USZipCodeField(blank=True)

    def __str__(self):
        return f'Location{self.id}'        

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # one to one relationship with user, CASCADE means if user is deleted, delete profile
    photo = models.ImageField(upload_to = user_directory_path , null=True) # upload_to is the path to upload the image to, blank=True means it is not required
    bio = models.TextField(max_length=150, blank=True) # blank=True means it is not required
    phone_number = models.CharField(max_length=12, blank=True)
    #then apply migration
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)
    #then apply migration again 
    #then go to admin.py and register the model
    #then go to views.py and add the profile to the context

    def __str__(self):
        return f'{self.user.username}\'s Profile' # this is what will be displayed in the admin page
        