from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.messaging_rooms, name="rooms"),
    path("<slug:room_slug>/", views.group_chat, name="group_chat"),
    path("direct/<int:user_id>/", views.direct_chat_room, name="direct_chat_room"),
]   
