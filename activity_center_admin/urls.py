from django.urls import path
from . import views

app_name = 'activity_center_admin'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Clubs CRUD
    path('clubs/', views.ClubListView.as_view(), name='club_list'),
    path('clubs/create/', views.ClubCreateView.as_view(), name='club_create'),
    path('clubs/<int:pk>/update/', views.ClubUpdateView.as_view(), name='club_update'),
    path('clubs/<int:pk>/delete/', views.ClubDeleteView.as_view(), name='club_delete'),
    
    # Events CRUD
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    
    # Club Activities Actions
    path('activities/', views.ActivityListView.as_view(), name='activity_list'),
    path('activities/<int:activity_id>/approve/', views.activity_approve, name='activity_approve'),
    path('activities/<int:activity_id>/reject/', views.activity_reject, name='activity_reject'),
    path('activities/<int:activity_id>/schedule-meeting/', views.schedule_meeting, name='schedule_meeting'),
    
    # Announcements Actions
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('announcements/<int:announcement_id>/approve/', views.announcement_approve, name='announcement_approve'),
    path('announcements/<int:announcement_id>/reject/', views.announcement_reject, name='announcement_reject'),
]
