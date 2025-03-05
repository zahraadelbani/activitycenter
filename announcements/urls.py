from django.urls import path
from . import views
app_name = 'announcements' 

urlpatterns = [
    path('list_announcements/', views.list_announcements, name='list_announcements'),
]
