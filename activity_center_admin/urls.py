from django.urls import path
from activity_center_admin import views
from voting.views import live_results

app_name = 'activity_center_admin'

urlpatterns = [
    # Dashboard
    path('', views.activity_admin_dashboard, name='dashboard'),

    # Club Management
    path('clubs/', views.ClubListView.as_view(), name='club_list'),
    path('clubs/create/', views.ClubCreateView.as_view(), name='club_create'),
    path('clubs/<int:pk>/update/', views.ClubUpdateView.as_view(), name='club_update'),
    path('clubs/<int:pk>/delete/', views.ClubDeleteView.as_view(), name='club_delete'),

    # Event Management
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    # Event Actions (Approve/Reject/Schedule)
    path('events/<int:activity_id>/approve/', views.event_approve, name='event_approve'),
    path('events/<int:activity_id>/reject/', views.event_reject, name='event_reject'),
    path('events/<int:activity_id>/schedule-meeting/', views.schedule_meeting, name='schedule_meeting'),

    # Announcements
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('announcements/<int:announcement_id>/approve/', views.announcement_approve, name='announcement_approve'),
    path('announcements/<int:announcement_id>/reject/', views.announcement_reject, name='announcement_reject'),

    # Nominations
    path('nominations/', views.manage_nominations, name='manage_nominations'),
    path('nominations/<int:candidate_id>/approve/', views.approve_nomination, name='approve_nomination'),
    path('nominations/<int:candidate_id>/reject/', views.reject_nomination, name='reject_nomination'),

    # Elections
    path('elections/', views.manage_elections, name='manage_elections'),
    path('elections/create/', views.create_election, name='create_election'),
    path('elections/<int:election_id>/edit/', views.edit_election, name='edit_election'),
    path('elections/<int:election_id>/delete/', views.delete_election, name='delete_election'),
    path('elections/<int:election_id>/toggle-active/', views.toggle_election_active, name='toggle_election_active'),
        path("elections/<int:election_id>/live-results/", live_results, name="live_results"),

]
