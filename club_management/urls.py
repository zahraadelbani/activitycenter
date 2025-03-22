from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from users.views import navbar
from users.views_auth import redirect_after_login 

urlpatterns = [
    path('redirect-after-login/', redirect_after_login, name='redirect_after_login'),
    path('', lambda request: redirect('accounts/login/')),  
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('activity-center-admin/', include('activity_center_admin.urls')),
    path('club-leader/', include('club_leader.urls')),
    #('rector/', include('rector.urls')),
    path('accounts/', include('allauth.urls')),
    path('club-member/', include('club_member.urls')),
    path('polls/', include('polls.urls')),
    path('navbar/', navbar, name='navbar'),
    path('', include('voting.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
