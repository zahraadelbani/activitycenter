from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', lambda request: HttpResponseRedirect('/users/list/')),
    path('activity-center-admin/', include('activity_center_admin.urls')),
    path('club-leader/', include('club_leader.urls')),
    path('rector/', include('rector.urls')),  # Redirect to the users list
    path('accounts/', include('allauth.urls')),  # AllAuth social logins
    path('users/', include('users.urls_auth')),  # Custom authentication
    path('club-member/', include('club_member.urls')),
    path('polls/', include('polls.urls')),
]
