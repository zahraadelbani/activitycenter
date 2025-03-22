from django.urls import path
from .consumers import VoteConsumer

websocket_urlpatterns = [
    path("ws/election/<int:election_id>/", VoteConsumer.as_asgi()),
]
