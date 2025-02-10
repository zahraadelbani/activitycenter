from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from club_leader.forms import ActivityRequestForm
from users.models import ClubLeader, User  # Use existing ClubLeader from users app
from club_member.models import MembershipTerminationRequest
from clubs.models import Announcement, ClubActivity
from feedback.models import Feedback
from analytics.models import ClubAnalytics

# Club Leader Dashboard
def club_leader_dashboard(request):
    """Club Leader Dashboard"""
    leader = get_object_or_404(ClubLeader, id=request.user.id)
    club = leader.club  # Ensure club exists before proceeding

    termination_requests = MembershipTerminationRequest.objects.filter(club=club, status="pending")
    announcements = Announcement.objects.filter(club=club, status="pending")
    feedbacks = Feedback.objects.filter(club=club, status="pending")

    analytics = None  # Prevent errors if analytics entry does not exist
    if club:
        analytics, created = ClubAnalytics.objects.get_or_create(club=club)
        analytics.update_stats()

    context = {
        "termination_requests": termination_requests,
        "announcements": announcements,
        "feedbacks": feedbacks,
        "analytics": analytics,
    }
    return render(request, "club_leader/dashboard.html", context)


# Approve/Reject Membership Termination Requests
def approve_termination_request(request, request_id):
    request_obj = get_object_or_404(MembershipTerminationRequest, id=request_id, club=request.user.club)
    request_obj.status = "approved"
    request_obj.save()
    messages.success(request, "Membership termination request approved.")
    return redirect("club_leader_dashboard")

def reject_termination_request(request, request_id):
    request_obj = get_object_or_404(MembershipTerminationRequest, id=request_id, club=request.user.club)
    request_obj.status = "rejected"
    request_obj.save()
    messages.error(request, "Membership termination request rejected.")
    return redirect("club_leader_dashboard")

# Approve/Reject Announcements
def approve_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id, club=request.user.club)
    announcement.status = "approved"
    announcement.save()
    messages.success(request, "Announcement approved.")
    return redirect("club_leader_dashboard")

def reject_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id, club=request.user.club)
    announcement.status = "rejected"
    announcement.save()
    messages.error(request, "Announcement rejected.")
    return redirect("club_leader_dashboard")

# Review Feedback
def review_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id, club=request.user.club)
    feedback.status = "reviewed"
    feedback.save()
    messages.success(request, "Feedback marked as reviewed.")
    return redirect("club_leader_dashboard")

# Club Analytics View
def club_analytics(request):
    """View analytics for the Club Leader's club"""
    leader = get_object_or_404(ClubLeader, id=request.user.id)
    
    # Ensure the leader has a valid club before proceeding
    if not leader.club:
        return render(request, "club_leader/analytics.html", {"error": "No club assigned to this leader."})

    club = leader.club

    analytics, created = ClubAnalytics.objects.get_or_create(club=club)
    analytics.update_stats()

    return render(request, "club_leader/analytics.html", {"analytics": analytics})

# ✅ Submit Activity Request
def submit_activity_request(request):
    if request.method == 'POST':
        form = ActivityRequestForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.approval_status = 'pending'  # Default status
            activity.save()
            messages.success(request, "Activity request submitted successfully!")
            return redirect('club_leader_dashboard')
    else:
        form = ActivityRequestForm()
    return render(request, 'club_leader/submit_activity_request.html', {'form': form})

# ✅ Approve/Reject Activity Request
def approve_activity_request(request, activity_id):
    activity = get_object_or_404(ClubActivity, id=activity_id)
    activity.approval_status = 'approved'
    activity.save()
    messages.success(request, "Activity request approved.")
    return redirect('club_leader_dashboard')

def reject_activity_request(request, activity_id):
    activity = get_object_or_404(ClubActivity, id=activity_id)
    activity.approval_status = 'rejected'
    activity.save()
    messages.error(request, "Activity request rejected.")
    return redirect('club_leader_dashboard')
