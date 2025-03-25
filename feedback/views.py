from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Feedback
from clubs.models import Club
from users.models import Membership
@login_required
def submit_feedback(request):
    user = request.user

    # Only fetch clubs the user is actively part of (member or leader)
    user_clubs = Club.objects.filter(
        memberships__user=user,
        memberships__membership_type__in=["member", "leader"]
    ).distinct()

    if request.method == "POST":
        club_id = request.POST.get("club_id")
        content = request.POST.get("content")
        category = request.POST.get("category")

        # Validate club membership
        club = get_object_or_404(user_clubs, id=club_id)

        if category not in ['complaint', 'suggestion']:
            return render(request, "feedback/submit_feedback.html", {
                "error": "Invalid category selected.",
                "clubs": user_clubs
            })

        Feedback.objects.create(
            club=club,
            submitted_by=None if category == "complaint" else user,
            content=content,
            category=category
        )

        return redirect("club_member:dashboard") 

    return render(request, "feedback/submit_feedback.html", {
        "clubs": user_clubs
    })