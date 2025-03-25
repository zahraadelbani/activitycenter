from django.shortcuts import render, get_object_or_404
from .models import Club

def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    return render(request, "clubs/club_detail.html", {"club": club})
