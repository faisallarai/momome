from django.contrib import admin

from .models import Transfer, Recipient, Transaction

# Register your models here.
admin.site.register((Transfer,Recipient,Transaction,))