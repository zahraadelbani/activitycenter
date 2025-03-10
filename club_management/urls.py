from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.conf.urls.static import static
from users.views import dashboard 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', lambda request: HttpResponseRedirect('/accounts/login/')),
    path('activity-center-admin/', include('activity_center_admin.urls')),
    path('club-leader/', include('club_leader.urls')),
    path('rector/', include('rector.urls')),  # Redirect to the users list
    path('accounts/', include('allauth.urls')),  # AllAuth social logins
    path('users/', include('users.urls_auth')),  # Custom authentication
    path('club-member/', include('club_member.urls')),
    path('polls/', include('polls.urls')),
    #path('events/', include('events.urls', namespace='events')), 
    #path('announcements/', include('announcements.urls', namespace='announcements')), 
    path('dashboard/', dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)