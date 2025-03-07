from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from club_leader.forms import ActivityRequestForm, ClubDocumentForm
from users.models import ClubLeader, User  
from club_member.models import MembershipTerminationRequest
from clubs.models import Announcement, ClubActivity, ClubDocument
from feedback.models import Feedback
from analytics.models import ClubAnalytics

from clubs.models import ClubDocument  # Import the model

def dashboard(request):
    """Club Leader Dashboard"""
    leader = get_object_or_404(ClubLeader, id=request.user.id)
    club = leader.club
    documents = ClubDocument.objects.filter(club=club)

    termination_requests = MembershipTerminationRequest.objects.filter(club=club, status="pending")
    announcements = Announcement.objects.filter(club=club, status="pending")
    feedbacks = Feedback.objects.filter(club=club, status="pending")

    analytics, created = ClubAnalytics.objects.get_or_create(club=club)
    analytics.update_stats()

    context = {
        "termination_requests": termination_requests,
        "announcements": announcements,
        "feedbacks": feedbacks,
        "analytics": analytics,
        "members_percentage": analytics.members_percentage(),  # Pass percentage
        "documents": documents,
        "club": club,
    }
    return render(request, 'club_leader/dashboard.html', context)




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


#@login_required
def upload_document(request):
    if request.user.get_role() != "Club Leader":
        raise PermissionDenied
    leader = get_object_or_404(ClubLeader, id=request.user.id)
    if request.method == 'POST':
        form = ClubDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.club = leader.club  # Assign the club manually
            print("Leader's Club:", leader.club)
            document.save()
            return redirect('club_leader:club_leader_dashboard')
    else:
        form = ClubDocumentForm()
    return render(request, 'club_leader/upload_document.html', {'form': form})

#@login_required
def delete_document(request, pk):
    document = get_object_or_404(ClubDocument, pk=pk)
    if request.user.get_role() != "Club Leader":
        raise PermissionDenied
    document.delete()
    return redirect('club_leader:club_leader_dashboard')

#@login_required
def list_documents(request):
    if request.user.get_role() not in ["Club Leader", "Club Member"]:
        raise PermissionDenied
    documents = ClubDocument.objects.filter(is_approved=True)
    return render(request, 'club_leader/document_list.html', {'documents': documents})

# @login_required
def list_resources(request):
    return render(request, 'club_leader/list_resources.html')
