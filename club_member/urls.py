from django.urls import path
from . import views

app_name = "club_member"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("join/", views.join_club, name="join_club"),
    path("leave/<int:club_id>/", views.leave_club, name="leave_club"),
    path("events/", views.view_events, name="events"),
    # path("attend-event/<int:event_id>/", views.attend_event, name="attend_event"),
    #path("vote/<int:club_id>/", views.vote_leader, name="vote_leader"),
    # path("feedback/", views.submit_feedback, name="submit_feedback"),
    path("documents/", views.view_documents, name="documents"),
    # path("messages/", views.messages, name="messages"),
    # path("club-chat/<int:club_id>/", views.club_chat, name="club_chat"),
    
    # Temporarily removed views that are not implemented yet
    # path("private-chat/<int:user_id>/", views.private_chat, name="private_chat"),
    # path("polls/", views.polls, name="polls"),
    # path("vote-poll/<int:poll_id>/", views.vote_poll, name="vote_poll"),
    # path("forum/<int:club_id>/", views.forum, name="forum"),
    # path("suggestions/", views.suggestions, name="suggestions"),
    
    path("cancel-termination-request/<int:request_id>/", views.cancel_termination_request, name="cancel_termination_request"),
]
