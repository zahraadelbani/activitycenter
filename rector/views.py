from django.shortcuts import render
from clubs.models import Club
from clubs.models import Announcement  # ✅ Correct import

def dashboard(request):
    clubs = Club.objects.all()  # Example: Rector oversees all clubs
    announcements = Announcement.objects.filter(status='pending')
    return render(request, 'rector/dashboard.html', {
        'clubs': clubs,
        'announcements': announcements,
    })
