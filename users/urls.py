from django.urls import path
from . import views
from .views_auth import login_view, logout_view  # Import your authentication views
from .views import dashboard,signup_view  # Import other views like dashboard


urlpatterns = [
  path('login/', login_view, name='login'),
  path("signup/", signup_view, name="signup"),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),  # Example protected route
    path('list/', views.list_users, name='list_users'),
    path('create/', views.create_user, name='create_user'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
