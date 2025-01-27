from django.shortcuts import render
from clubs.models import ClubActivity

def dashboard(request):
    # Customize this for club leaders
    club_activities = ClubActivity.objects.filter(club__leader=request.user)
    return render(request, 'club_leader/dashboard.html', {
        'club_activities': club_activities,
    })
