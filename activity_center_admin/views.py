from django.shortcuts import render
from clubs.models import Club, ClubActivity
from announcements.models import Announcement

def dashboard(request):
    clubs = Club.objects.all()
    activities = ClubActivity.objects.filter(status='pending')
    announcements = Announcement.objects.filter(status='pending')
    return render(request, 'activity_center_admin/dashboard.html', {
        'clubs': clubs,
        'activities': activities,
        'announcements': announcements,
    })
