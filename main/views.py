from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from .forms import ListingForm
from .models import LikedListing, Listing
from .filters import ListingFilter

from users.forms import LocationForm
from imp import reload

from django.shortcuts import get_object_or_404
# Create your views here.

def landing_view(request):
    return render(request, 'views/main.html',{"name":"AutoMax"})

@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(profile=request.user.profile).values_list('listing')
    liked_listing_ids = [l[0] for l in user_liked_listings]
    context = {
        'listing_filter': listing_filter,
        'liked_listing_ids': liked_listing_ids,
    }
    return render(request, 'views/home.html',context)

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()
                messages.info(
                    request, f'{listing.model} Listing created successfully!')
                return redirect('home')
            else:
                raise Exception('Invalid form data')
        except Exception as e: 
            print(e)
            messages.error(request, 'An error has occured during listing. Please try again.')
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request, 'views/list.html',{'listing_form':listing_form , 'location_form':location_form, }) #BIG MISTAKE IF YOU PUT FORMS SEPRATELY

@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception('Invalid Listing ID')
        return render(request, 'views/listing.html',{'listing':listing}, )
    except Exception as e:
        messages.error(request, f'An Invalid UID {id} was passed. Please try again.')
        return redirect('home')
    
@login_required
def edit_view(request, id): 
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = ListingForm(
                request.POST, request.FILES, instance=listing)
            location_form = LocationForm(
                request.POST, instance=listing.location)
            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()
                location_form.save()
                messages.info(
                    request, f'Listing {id} edited successfully!')
                return redirect('home')
            else:
                messages.error(
            request, 'An error has occured editing listing. Please try again.')
                return reload()
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
        context = {
            'listing_form': listing_form,
            'location_form': location_form,
        }
        return render(request, 'views/edit.html' , context)
    except Exception as e:
        messages.error(
            request, 'An error has occured trying to access the edit page.')
        return redirect('home')

@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)
    
    liked_Listing, created = LikedListing.objects.get_or_create(profile=request.user.profile, listing=listing)

    if not created:
        liked_Listing.delete()
    else:
        liked_Listing.save()

    return JsonResponse({
        'is_liked_by_user': created,})

@login_required
def inquire_listing_using_email(request, id):
    listing = get_object_or_404(Listing, id=id)
    try:
        emailSubject = f'{request.user.profile} is interested in your {listing.model} listing'
        emailMessage = f'Hi {listing.seller},\n\n{request.user.profile} is interested in your {listing.model} listing. Please contact them at {request.user.email}.\n\nThanks,\nAutoMax'
        send_mail(emailSubject, emailMessage, 'noreply@automax.com', [listing.seller.user.email], fail_silently=True,)
        return JsonResponse({
        "success":True,
    })
    except Exception as e:
        print(e)
    return JsonResponse({
        "success":False,
        "info": e,
    })