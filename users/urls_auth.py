from django.urls import path
from .views_auth import login_view, logout_view  # Ensure you have views_auth.py

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
