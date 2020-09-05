from authentication.views import profile,ProfileUpdate
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = 'authentication'

urlpatterns = [
    path('',profile,name = 'profile'),
    path('update/<slug:slug>/',ProfileUpdate.as_view(),name = 'update'),
    path('loginpop/', auth_views.LoginView.as_view(template_name='loginpop.html'),name = 'loginpop'),
]