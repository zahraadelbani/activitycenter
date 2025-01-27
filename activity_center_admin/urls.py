from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='activity_center_admin_dashboard'),
]
