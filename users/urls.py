from django.urls import path
from . import views
from .views import CustomSignupView, dashboard, base_view, profile_view

app_name = "users" 

urlpatterns = [
    path('base/', base_view, name='base'),
    path("profile/", profile_view, name="profile"),
    path('dashboard/', dashboard, name='dashboard'),
    path('list/', views.list_users, name='list_users'),
    path('create/', views.create_user, name='create_user'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path("accounts/signup/", CustomSignupView.as_view(), name="account_signup"),
]
