from django.urls import path
from .views import list_events, create_event, update_event, delete_event

urlpatterns = [
    path("", list_events, name="list_events"),
    path("create/", create_event, name="create_event"),
    path("<int:event_id>/edit/", update_event, name="update_event"),
    path("<int:event_id>/delete/", delete_event, name="delete_event"),
]
