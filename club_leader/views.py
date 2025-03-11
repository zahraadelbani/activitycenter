from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils.timezone import now
from club_leader.forms import AnnouncementForm, ClubDocumentForm, EventRequestForm
from users.models import ClubLeader, User,ClubMember  
from club_member.models import MembershipTerminationRequest
from clubs.models import Announcement, ClubDocument, Event, RescheduleRequest
from feedback.models import Feedback
from analytics.models import ClubAnalytics

@login_required
def dashboard(request):
    """Club Leader Dashboard"""

    leader = get_object_or_404(ClubLeader, id=request.user.id)
    club = leader.club
    documents = ClubDocument.objects.filter(club=club)

    # Fetch membership termination requests
    termination_requests = MembershipTerminationRequest.objects.filter(club=club, status="pending")

    # Fetch feedback (Complaints & Suggestions separately)
    complaints = Feedback.objects.filter(club=club, category="complaint", status="pending")
    suggestions = Feedback.objects.filter(club=club, category="suggestion", status="pending")

    pending_events = Event.objects.filter(club=club, approval_status="pending")


    # Fetch announcements & analytics
    announcements = Announcement.objects.filter(club=club)
    analytics, created = ClubAnalytics.objects.get_or_create(club=club)
    analytics.update_stats()

    context = {
        "termination_requests": termination_requests,
        "announcements": announcements,
        "complaints": complaints,
        "suggestions": suggestions,
        "analytics": analytics,
        "members_percentage": analytics.members_percentage(),
        "documents": documents,
        "club": club,
        "pending_events": pending_events,
    }
    
    return render(request, 'club_leader/dashboard.html', context)


@login_required
def review_feedback(request, feedback_id):
    #Marks a feedback entry as reviewed by the club leader.

    # Get the ClubLeader instance using `email`
    try:
        leader = ClubLeader.objects.get(email=request.user.email)
    except ClubLeader.DoesNotExist:
        messages.error(request, "You are not assigned as a club leader.")
        return redirect("club_leader_dashboard")  

    club = leader.club  # ✅ Get the associated club

    # Retrieve the feedback related to this club
    feedback = get_object_or_404(Feedback, id=feedback_id, club=club)

    # Update the status to "reviewed"
    feedback.status = "reviewed"
    feedback.save()

    messages.success(request, "Feedback marked as reviewed.")
    return redirect("club_leader:club_leader_dashboard")  




@login_required
def club_members(request):
    """Displays all members of the club leader's club."""
    
    # Get the club leader's club
    leader = get_object_or_404(ClubLeader, id=request.user.id)

    if not leader.club:
        return render(request, "club_leader/members.html", {"error": "You are not assigned to any club."})

    # Get members of the club
    members = ClubMember.objects.filter(club=leader.club)

    return render(request, "club_leader/members.html", {"members": members, "club": leader.club})

@login_required
def remove_member(request, member_id):
    """Allows the club leader to remove a member from their club."""
    
    leader = get_object_or_404(ClubLeader, id=request.user.id)

    if not leader.club:
        messages.error(request, "You are not assigned to a club.")
        return redirect("club_leader:club_members")

    member = get_object_or_404(ClubMember, id=member_id, club=leader.club)

    if request.method == "POST":
        member.delete()
        messages.success(request, "Member successfully removed from the club.")
        return redirect("club_leader:club_members")

    raise PermissionDenied

@login_required
def termination_requests(request):
    """Displays all pending termination requests for the club leader's club."""
    
    leader = get_object_or_404(ClubLeader, id=request.user.id)

    if not leader.club:
        return render(request, "club_leader/termination_requests.html", {"error": "You are not assigned to a club."})

    requests = MembershipTerminationRequest.objects.filter(club=leader.club, status="pending")

    return render(request, "club_leader/termination_requests.html", {"requests": requests, "club": leader.club})

# Approve/Reject Membership Termination Requests
@login_required
def approve_termination_request(request, request_id):
    """Approves a membership termination request and removes the member from the club."""
    request_obj = get_object_or_404(MembershipTerminationRequest, id=request_id, club=request.user.clubleader.club)

    # Get the member instance from `users.ClubMember`
    member = get_object_or_404(ClubMember, id=request_obj.club_member.id)

    # Step 1: Update the termination request status first
    request_obj.status = "approved"
    request_obj.reviewed_at = now()
    request_obj.save()  # Save the request update BEFORE deleting the member

    # Step 2: Now safely delete the member
    member.delete()

    messages.success(request, "Membership termination request approved. The member has been removed from the club.")
    return redirect("club_leader:termination_requests") 



@login_required
def reject_termination_request(request, request_id):
    """Rejects a membership termination request."""
    request_obj = get_object_or_404(MembershipTerminationRequest, id=request_id, club=request.user.clubleader.club)
    request_obj.status = "rejected"
    request_obj.reviewed_at = now()  # Record the review time
    request_obj.save()

    messages.error(request, "Membership termination request rejected.")
    return redirect("club_leader:termination_requests")  # Redirect to the new termination requests page


# Approve/Reject Announcements
""" def approve_announcement(request, announcement_id):
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
    return redirect("club_leader_dashboard") """

# Review Feedback
""" def review_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id, club=request.user.club)
    feedback.status = "reviewed"
    feedback.save()
    messages.success(request, "Feedback marked as reviewed.")
    return redirect("club_leader_dashboard") """

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

@login_required
def submit_event_request(request):
    """Handles event creation by club leaders."""

    # Ensure the user is a Club Leader
    if not ClubLeader.objects.filter(id=request.user.id).exists():
        return redirect('club_leader:dashboard')  # Unauthorized users redirected

    leader = ClubLeader.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = EventRequestForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = leader.club  # Automatically assign club
            event.created_by = request.user
            event.approval_status = 'pending'
            event.save()
            return redirect('club_leader:calendar')

    return redirect('club_leader:calendar') 

# Approve/Reject Event Request
def approve_event_request(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.approval_status = 'approved'
    event.save()
    messages.success(request, "Event request approved.")
    return redirect('club_leader_dashboard')

def reject_event_request(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.approval_status = 'rejected'
    event.save()
    messages.error(request, "Event request rejected.")
    return redirect('club_leader_dashboard')


#activity center rescheduling 
def request_reschedule(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if not request.user.groups.filter(name='ActivityCenterAdmin').exists():
        raise PermissionDenied

    reschedule, created = RescheduleRequest.objects.get_or_create(event=event, club_leader=event.club.leader)
    messages.success(request, "Reschedule request sent to the club leader.")
    return redirect('pending_events')

def approve_reschedule(request, reschedule_id):
    reschedule = get_object_or_404(RescheduleRequest, id=reschedule_id)

    if not request.user.groups.filter(name='ActivityCenterAdmin').exists():
        raise PermissionDenied

    reschedule.status = "approved"
    reschedule.event.rescheduled = True
    reschedule.event.save()
    reschedule.save()
    messages.success(request, "Event reschedule approved.")
    return redirect('pending_events')



#@login_required
def upload_document(request):
    """Allow club leaders to upload documents"""
    if request.user.get_role() != "Club Leader":
        raise PermissionDenied

    leader = get_object_or_404(ClubLeader, id=request.user.id)
    
    if request.method == 'POST':
        form = ClubDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.club = leader.club  # Assign club
            document.uploaded_by = request.user  # Assign uploader
            document.save()
            messages.success(request, "Document uploaded successfully!")
            return redirect('club_leader:list_documents')
    else:
        form = ClubDocumentForm()

    return render(request, 'club_leader/upload_document.html', {'form': form})


#@login_required
def delete_document(request, pk):
    """Delete a document (Club Resource)"""
    document = get_object_or_404(ClubDocument, pk=pk)

    # Ensure only the club leader can delete documents from their own club
    if request.user.get_role() != "Club Leader" or document.club != request.user.clubleader.club:
        raise PermissionDenied

    document.delete()
    messages.success(request, "Document deleted successfully!")
    return redirect('club_leader:list_documents')


#@login_required
def list_documents(request):
    """List all documents (club resources) for the club leader and members"""
    if request.user.get_role() not in ["Club Leader", "Club Member"]:
        raise PermissionDenied

    leader = get_object_or_404(ClubLeader, id=request.user.id)
    documents = ClubDocument.objects.filter(club=leader.club)

    return render(request, 'club_leader/list_documents.html', {'documents': documents})

# Create an Announcement (Club Leaders Only)
def create_announcement(request):
    if request.user.get_role() != "Club Leader":
        raise PermissionDenied

    leader = get_object_or_404(ClubLeader, id=request.user.id)

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.club = leader.club  # Assign to club
            announcement.save()
            messages.success(request, "Announcement created successfully!")
            return redirect("club_leader:list_announcements")
    else:
        form = AnnouncementForm()

    return render(request, "club_leader/create_announcement.html", {"form": form})

# List Announcements (For Club Members & Leaders)
def list_announcements(request):
    """List all announcements for a specific club."""
    leader = get_object_or_404(ClubLeader, id=request.user.id)
    announcements = Announcement.objects.filter(club=leader.club).order_by("-created_at")

    return render(request, "club_leader/list_announcements.html", {"announcements": announcements})

# Delete an Announcement (Club Leaders Only)
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.user.get_role() != "Club Leader" or announcement.club != request.user.clubleader.club:
        raise PermissionDenied

    announcement.delete()
    messages.success(request, "Announcement deleted successfully!")
    return redirect("club_leader:list_announcements")

# Edit an Announcement (Club Leaders Only)
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.user.get_role() != "Club Leader" or announcement.club != request.user.clubleader.club:
        raise PermissionDenied

    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated successfully!")
            return redirect("club_leader:list_announcements")
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, "club_leader/edit_announcement.html", {"form": form})

# Toggle Announcement Visibility (Club Leaders Only)
def toggle_visibility(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.user.get_role() != "Club Leader" or announcement.club != request.user.clubleader.club:
        raise PermissionDenied

    announcement.visible = not announcement.visible  # Toggle visibility
    announcement.save()
    messages.success(request, f"Announcement is now {'visible' if announcement.visible else 'hidden'}.")
    return redirect("club_leader:list_announcements")

#calendar of events
@login_required
def event_calendar(request):
    """Renders the club leader's event calendar."""

    if not ClubLeader.objects.filter(id=request.user.id).exists():
        return redirect('club_leader:dashboard')  

    leader = ClubLeader.objects.get(id=request.user.id)
    events = Event.objects.filter(club=leader.club).order_by('event_date')  
    form = EventRequestForm()  

    return render(request, 'club_leader/calendar.html', {'events': events, 'form': form})

@login_required
def get_events(request):
    # Example: only fetch the current user's club events
    if not ClubLeader.objects.filter(id=request.user.id).exists():
        return JsonResponse({"error": "Unauthorized"}, status=403)

    leader = ClubLeader.objects.get(id=request.user.id)
    events = Event.objects.filter(club=leader.club)

    # Format them for FullCalendar
    event_list = []
    for e in events:
        event_list.append({
            "title": e.title,
            "start": e.event_date.isoformat(),  # key is 'start' for FullCalendar
            "approval_status": e.approval_status,  # custom field
        })

    return JsonResponse(event_list, safe=False)

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure only the club leader who created the event can edit it
    if request.user != event.created_by:
        raise PermissionDenied

    if request.method == "POST":
        form = EventRequestForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully! Approval required.")
            return redirect("club_leader:calendar")  # Redirect to event calendar

    else:
        form = EventRequestForm(instance=event)

    return render(request, "club_leader/edit_event.html", {"form": form, "event": event})
