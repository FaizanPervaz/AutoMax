from django.contrib import admin
from .models import Listing,LikedListing
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',) # This is to make the id field read-only, can't change it anymore

class LikedListingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',) # This is to make the id field read-only, can't change it anymore

admin.site.register(Listing, ListingAdmin)
admin.site.register(LikedListing, LikedListingAdmin)
