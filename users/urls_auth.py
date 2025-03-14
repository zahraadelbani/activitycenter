from django.urls import path
from .views_auth import login_view, signup_view, custom_logout_view
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', login_view, name='account_login'),
    path('signup/', signup_view, name='account_signup'),
    path('logout/', custom_logout_view, name='account_logout'),
]
