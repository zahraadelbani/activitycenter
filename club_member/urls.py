from django.urls import path

from feedback.views import submit_feedback
from . import views

app_name = "club_member"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("join/", views.join_club, name="join_club"),
    path("leave/<int:club_id>/", views.leave_club, name="leave_club"),
    path("events/", views.view_events, name="events"),
    path("calendar/", views.event_calendar_member, name="event_calendar"),
    path("get-events/", views.get_events_member, name="get_events_member"),
    path("remind/<int:event_id>/", views.remind_me, name="remind_me"),
    path("member-announcements/", views.member_announcements, name="member_announcements"),
    path('contact/', views.contact, name='contact'),



    # path("attend-event/<int:event_id>/", views.attend_event, name="attend_event"),
    #path("vote/<int:club_id>/", views.vote_leader, name="vote_leader"),
    path("feedback/", submit_feedback, name="submit_feedback"),
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
    path('faq/', views.faq_user_member, name='faq_user_member'),
   path('debug-time/', views.debug_time, name='debug_time'),



]
