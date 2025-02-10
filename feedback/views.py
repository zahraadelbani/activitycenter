from django.shortcuts import render, redirect
from .models import Feedback
from clubs.models import Club
from users.models import User

def submit_feedback(request):
    """Allows club members to submit complaints (anonymous) or suggestions (with user info)."""
    if request.method == "POST":
        club_id = request.POST.get("club_id")
        content = request.POST.get("content")
        category = request.POST.get("category")  # Either 'complaint' or 'suggestion'

        club = Club.objects.get(id=club_id)

        if category == "complaint":
            # ✅ Create an anonymous complaint
            Feedback.objects.create(club=club, content=content, category=category)
        else:
            # ✅ Create a suggestion linked to the user
            Feedback.objects.create(club=club, submitted_by=request.user, content=content, category=category)

        return redirect("club_dashboard")

    return render(request, "feedback/submit_feedback.html")
