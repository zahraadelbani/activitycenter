from django.urls import path
from . import views
app_name = 'events' 

urlpatterns = [
    path('create/', views.create_event, name='create_event'),
    path('list/', views.list_events, name='list_events'),
    path("create/", views.create_event, name="create_event"),
    path("<int:event_id>/edit/", views.update_event, name="update_event"),
    path("<int:event_id>/delete/", views.delete_event, name="delete_event"),
]
