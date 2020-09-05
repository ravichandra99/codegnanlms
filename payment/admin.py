from django.contrib import admin

from .models import Order, Checkout

# Register your models here.

admin.site.register(Order)
admin.site.register(Checkout)
