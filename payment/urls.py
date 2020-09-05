from django.contrib.auth import views as auth_views
from django.urls import path

from .views import make_order, checkout_success, Payment

app_name = 'payment'

urlpatterns = [
    path('', Payment.as_view(), name='payment'),
    path('order/', make_order, name='order'),
    path('success/<slug:slug>', checkout_success, name='success'),
]
