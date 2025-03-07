from django.urls import path
from . import views

app_name = 'club_leader'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path("dashboard/", views.dashboard, name="club_leader_dashboard"),
    path("approve-termination/<int:request_id>/", views.approve_termination_request, name="approve_termination"),
    path("reject-termination/<int:request_id>/", views.reject_termination_request, name="reject_termination"),
    #path("approve-announcement/<int:announcement_id>/", views.approve_announcement, name="approve_announcement"),
    #path("reject-announcement/<int:announcement_id>/", views.reject_announcement, name="reject_announcement"),
    path("review-feedback/<int:feedback_id>/", views.review_feedback, name="review_feedback"),
    path("analytics/", views.club_analytics, name="club_analytics"),
    path("activity-request/", views.submit_activity_request, name="submit_activity_request"),
    path("activity-request/approve/<int:activity_id>/", views.approve_activity_request, name="approve_activity_request"),
    path("activity-request/reject/<int:activity_id>/", views.reject_activity_request, name="reject_activity_request"),
    path('upload-document/', views.upload_document, name='upload_document'),
    path('delete-document/<int:pk>/', views.delete_document, name='delete_document'),
    path('documents/', views.list_documents, name='list_documents'),
    path("announcements/", views.list_announcements, name="list_announcements"),
    path("announcements/create/", views.create_announcement, name="create_announcement"),
    path("announcements/edit/<int:pk>/", views.edit_announcement, name="edit_announcement"),  # ✅ Edit URL
    path("announcements/toggle/<int:pk>/", views.toggle_visibility, name="toggle_visibility"),  # ✅ Toggle URL
    path("announcements/delete/<int:pk>/", views.delete_announcement, name="delete_announcement"),
    path('submit-activity/', views.submit_activity_request, name='submit_activity_request'),

]
