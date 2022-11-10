from django.contrib import admin

from .models import Transfer, Recipient

# Register your models here.
admin.site.register((Transfer,Recipient,))