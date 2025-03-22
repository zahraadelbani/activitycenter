from django.urls import path
from . import views
from .views import profile_view,userdashboard

app_name = "users" 

urlpatterns = [
    path("profile/", profile_view, name="profile"),
    path('udashboard/', userdashboard, name='udashboard'),
    path('list/', views.list_users, name='list_users'),
    path('create/', views.create_user, name='create_user'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
