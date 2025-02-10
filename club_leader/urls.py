from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.club_leader_dashboard, name="club_leader_dashboard"),
    path("approve-termination/<int:request_id>/", views.approve_termination_request, name="approve_termination"),
    path("reject-termination/<int:request_id>/", views.reject_termination_request, name="reject_termination"),
    path("approve-announcement/<int:announcement_id>/", views.approve_announcement, name="approve_announcement"),
    path("reject-announcement/<int:announcement_id>/", views.reject_announcement, name="reject_announcement"),
    path("review-feedback/<int:feedback_id>/", views.review_feedback, name="review_feedback"),
    path("analytics/", views.club_analytics, name="club_analytics"),
    path("activity-request/", views.submit_activity_request, name="submit_activity_request"),
    path("activity-request/approve/<int:activity_id>/", views.approve_activity_request, name="approve_activity_request"),
    path("activity-request/reject/<int:activity_id>/", views.reject_activity_request, name="reject_activity_request"),

]
