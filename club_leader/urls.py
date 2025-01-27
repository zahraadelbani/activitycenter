from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='club_leader_dashboard'),
]
