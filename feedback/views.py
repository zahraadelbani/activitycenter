from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Feedback
from clubs.models import Club

@login_required
def submit_feedback(request):
    if request.method == "POST":
        club_id = request.POST.get("club_id")
        content = request.POST.get("content")
        category = request.POST.get("category")

        club = get_object_or_404(Club, id=club_id)

        if category not in ['complaint', 'suggestion']:
            return render(request, "feedback/submit_feedback.html", {
                "error": "Invalid category selected.",
                "clubs": Club.objects.all()
            })

        Feedback.objects.create(
            club=club,
            submitted_by=None if category == "complaint" else request.user,
            content=content,
            category=category
        )

        return redirect("club_dashboard")  # Adjust this URL as needed

    return render(request, "feedback/submit_feedback.html", {
        "clubs": Club.objects.all()  # Allow club selection if needed
    })
