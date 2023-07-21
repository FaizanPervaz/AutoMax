from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from main.models import LikedListing
from .forms import LocationForm, ProfileForm, UserForm
from main.models import Listing
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request = request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(
                    request, f'Welcome back {username}!')
                return redirect('home')
            else:
                messages.error(request,'An error has occured during login. Please try again.') 
        else:
            messages.error(request,'An error has occured during login. Please try again.') 
    elif request.method == 'GET':
        login_form = AuthenticationForm()
    return render(request, 'views/login.html',{'login_form':login_form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(
        request, f'You have been logged out successfully!')
    return redirect('main')

class RegisterView(View):
    def get(self, request):
        register_form = UserCreationForm()
        return render(request, 'views/register.html',{'register_form':register_form})
    def post(self, request):
        register_form = UserCreationForm(data = request.POST)
        if register_form.is_valid():
            user=register_form.save()
            user.refresh_from_db()        
            # password = register_form.cleaned_data.get('password')
            # user = authenticate(username=user.username,password=password)
            login(request,user)
            messages.success(
                request, f'Account created for {user.username} successfully!')
            return redirect('home')
        else:
            messages.error(request,'An error has occured during registration. Please try again.')
            return render(request, 'views/register.html',{'register_form':register_form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user_listings = Listing.objects.filter(seller = request.user.profile)
        user_liked_listings = LikedListing.objects.filter(
            profile = request.user.profile).all()
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        location_form = LocationForm(instance=request.user.profile.location)
        return render(request, 'views/profile.html',{'user_form':user_form,
                                                     'profile_form':profile_form,
                                                     'location_form':location_form,
                                                     'user_listings':user_listings,
                                                     'user_liked_listings':user_liked_listings,})

    def post(self, request):
        user_listings = Listing.objects.filter(seller = request.user.profile)
        user_liked_listings = LikedListing.objects.filter(
            profile = request.user.profile).all()
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        location_form = LocationForm(request.POST, instance=request.user.profile.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(
                request, f'Profile updated successfully!')
            return redirect('profile')
        else: 
            messages.error(request,'An error has occured during profile update. Please try again.')
            return render(request, 'views/profile.html',{'user_form':user_form,
                                                     'profile_form':profile_form,
                                                     'location_form':location_form,
                                                     'user_listings':user_listings,
                                                     'user_liked_listings':user_liked_listings,})


