from django.contrib import admin

from user.models import AddressInfo, CustomUser, UserProfile

# Register your models here.
admin.site.register((CustomUser, UserProfile, AddressInfo))