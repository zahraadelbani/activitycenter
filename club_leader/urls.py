from django.urls import path

from club_member.views import view_events
from . import views

app_name = 'club_leader'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path("dashboard/", views.dashboard, name="club_leader_dashboard"),
    path("termination-request/approve/<int:request_id>/", views.approve_termination_request, name="approve_termination"),
    path("termination-request/reject/<int:request_id>/", views.reject_termination_request, name="reject_termination"),
    #path("approve-announcement/<int:announcement_id>/", views.approve_announcement, name="approve_announcement"),
    #path("reject-announcement/<int:announcement_id>/", views.reject_announcement, name="reject_announcement"),
    #path("review-feedback/<int:feedback_id>/", views.review_feedback, name="review_feedback"),
    path("analytics/", views.club_analytics, name="club_analytics"),
    #path("activity-request/", views.submit_activity_request, name="submit_activity_request"),
    #path("activity-request/approve/<int:activity_id>/", views.approve_activity_request, name="approve_activity_request"),
    #path("activity-request/reject/<int:activity_id>/", views.reject_activity_request, name="reject_activity_request"),
    path('upload-document/', views.upload_document, name='upload_document'),
    path('delete-document/<int:pk>/', views.delete_document, name='delete_document'),
    path('documents/', views.list_documents, name='list_documents'),
    path("announcements/", views.list_announcements, name="list_announcements"),
    path("announcements/create/", views.create_announcement, name="create_announcement"),
    path("announcements/edit/<int:pk>/", views.edit_announcement, name="edit_announcement"),  # ✅ Edit URL
    path("announcements/toggle/<int:pk>/", views.toggle_visibility, name="toggle_visibility"),  # ✅ Toggle URL
    path("announcements/delete/<int:pk>/", views.delete_announcement, name="delete_announcement"),
    #path('submit-activity/', views.submit_activity_request, name='submit_activity_request'),


    path("event-request/", views.submit_event_request, name="submit_event_request"),
    path("event-request/approve/<int:event_id>/", views.approve_event_request, name="approve_event_request"),
    path("event-request/reject/<int:event_id>/", views.reject_event_request, name="reject_event_request"),


    path("event-request/reschedule/<int:event_id>/", views.request_reschedule, name="request_reschedule"),
    path("event-request/reschedule/approve/<int:reschedule_id>/", views.approve_reschedule, name="approve_reschedule"),

    path('calendar/', views.event_calendar, name='calendar'),
    path('submit-event/', views.submit_event_request, name='submit_event_request'),
    path('get-events/', views.get_events, name='get_events'), 
    path('event/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path("club-members/", views.club_members, name="club_members"),
    path("remove-member/<int:member_id>/", views.remove_member, name="remove_member"),
    path("termination-requests/", views.termination_requests, name="termination_requests"),
    path('review-feedback/<int:feedback_id>/', views.review_feedback, name='review_feedback'),




]
