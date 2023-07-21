import uuid
from django.db import models
from users.models import Profile,Location
from .consts import CAR_BRANDS,TRANSMISSION_OPTIONS
from.utils import user_listing_path
# Create your models here.
class Listing(models.Model):
    id=models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    seller=models.ForeignKey(Profile, on_delete=models.CASCADE) #bcoz of one to many relationship we are implementing this here as one user can have many listing
    brand = models.CharField(max_length=24, choices=CAR_BRANDS, default=None)
    model = models.CharField(max_length=64,)
    vin = models.CharField(max_length=17, unique=True)
    mileage = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=24)
    description = models.TextField(default=None)
    engine = models.CharField(max_length=24, default=None)
    transmission = models.CharField(max_length=24, choices=TRANSMISSION_OPTIONS, default=None)
    location = models.OneToOneField(Location,on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=user_listing_path)

    def __str__(self):
        return f'{self.seller.user.username}\'s - {self.brand} {self.model}'

class LikedListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username} liked {self.listing.model}'
