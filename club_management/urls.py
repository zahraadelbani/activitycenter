from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from users.views import dashboard 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('activity-center-admin/', include('activity_center_admin.urls')),
    path('club-leader/', include('club_leader.urls')),
    path('rector/', include('rector.urls')),
    path('accounts/', include('allauth.urls')),  # AllAuth for authentication
    path('users/auth/', include('users.urls_auth')),  # Custom authentication (overrides AllAuth)
    path('club-member/', include('club_member.urls')),
    path('polls/', include('polls.urls')),
    path('dashboard/', dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
