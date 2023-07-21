from django import forms
from django.contrib.auth.models import User
from .models import Location, Profile
from localflavor.us.forms import USStateField,USZipCodeField
from .widgets import CustomPictureImageFieldWidget

class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    class Meta:
        model = User
        fields = {'username','first_name','last_name'}    

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=CustomPictureImageFieldWidget)
    bio = forms.TextInput()

    class Meta:
        model = Profile
        fields = {'photo','bio','phone_number'}


class LocationForm(forms.ModelForm):
    address_1 = forms.CharField(required=True)
    zipcode = USZipCodeField(required=True)
    
    class Meta:
        model = Location
        fields = {'address_1','address_2','city','state','zipcode'}
