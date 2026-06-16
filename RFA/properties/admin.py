from django.contrib import admin

from properties.models import Facility, Property, PropertyImage, Wishlist

# Register your models here.
admin.site.register(Property)
admin.site.register(Facility)
admin.site.register(PropertyImage)
admin.site.register(Wishlist)