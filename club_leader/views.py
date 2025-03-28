from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils.timezone import now
from club_leader.decorators import get_leader_club
from club_leader.forms import AnnouncementForm, ClubDocumentForm, EventRequestForm
from users.models import User, Membership
from club_member.models import MembershipTerminationRequest
from clubs.models import Announcement, ClubDocument, Event, RescheduleRequest, Club
from feedback.models import Feedback
from analytics.models import ClubAnalytics
from django.core.paginator import Paginator



@login_required
def club_leader_dashboard(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized to access this dashboard.")

    documents = ClubDocument.objects.filter(club=club)
    termination_requests = MembershipTerminationRequest.objects.filter(club=club, status="pending")
    complaints = Feedback.objects.filter(club=club, category="complaint", status="pending").order_by('-created_at')
    suggestions = Feedback.objects.filter(club=club, category="suggestion", status="pending").order_by('-created_at')
    pending_events = Event.objects.filter(club=club, approval_status="pending")
    announcements = Announcement.objects.filter(club=club)
    analytics, _ = ClubAnalytics.objects.get_or_create(club=club)
    analytics.update_stats()

    # Pagination logic
    complaint_paginator = Paginator(complaints, 3)  # 3 per page
    suggestion_paginator = Paginator(suggestions, 3)

    complaints_page = complaint_paginator.get_page(request.GET.get("complaints_page"))
    suggestions_page = suggestion_paginator.get_page(request.GET.get("suggestions_page"))

    context = {
        "announcements": announcements,
        "complaints_page": complaints_page,
        "suggestions_page": suggestions_page,
        "analytics": analytics,
        "members_percentage": analytics.members_percentage(),
        "documents": documents,
        "club": club,
        "pending_events": pending_events,
    }
    return render(request, 'club_leader/dashboard.html', context)

@login_required
def review_feedback(request, feedback_id):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized to access this dashboard.")

    feedback = get_object_or_404(Feedback, id=feedback_id, club=club)
    feedback.status = "reviewed"
    feedback.save()
    messages.success(request, "Feedback marked as reviewed.")
    return redirect("club_leader:dashboard")

@login_required
def club_members(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    members = Membership.objects.filter(club=club, membership_type="member")
    return render(request, "club_leader/members.html", {"members": members, "club": club})

@login_required
def remove_member(request, member_id):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    member = get_object_or_404(Membership, id=member_id, club=club, membership_type="member")
    if request.method == "POST":
        member.delete()
        messages.success(request, "Member successfully removed from the club.")
        return redirect("club_leader:club_members")
    raise PermissionDenied

@login_required
def termination_requests(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    requests = MembershipTerminationRequest.objects.filter(club=club, status="pending")
    return render(request, "club_leader/termination_requests.html", {"requests": requests, "club": club})

@login_required
def approve_termination_request(request, request_id):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    request_obj = get_object_or_404(MembershipTerminationRequest, id=request_id, club=club)
    member = request_obj.membership
    request_obj.status = "approved"
    request_obj.reviewed_at = now()
    request_obj.save()
    member.delete()
    messages.success(request, "Membership termination request approved. The member has been removed from the club.")
    return redirect("club_leader:termination_requests")

@login_required
def reject_termination_request(request, request_id):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    request_obj = get_object_or_404(MembershipTerminationRequest, id=request_id, club=club)
    request_obj.status = "rejected"
    request_obj.reviewed_at = now()
    request_obj.save()
    messages.error(request, "Membership termination request rejected.")
    return redirect("club_leader:termination_requests")

@login_required
def club_analytics(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    analytics, created = ClubAnalytics.objects.get_or_create(club=club)
    analytics.update_stats()
    return render(request, "club_leader/analytics.html", {"analytics": analytics, "club": club})

@login_required
def submit_event_request(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    if request.method == 'POST':
        form = EventRequestForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club
            event.created_by = request.user
            event.approval_status = 'pending'
            event.save()
    return redirect('club_leader:calendar')

@login_required
def upload_document(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    if request.method == 'POST':
        form = ClubDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.club = club
            document.uploaded_by = request.user
            document.save()
            messages.success(request, "Document uploaded successfully!")
            return redirect('club_leader:list_documents')
    else:
        form = ClubDocumentForm()
    return render(request, 'club_leader/upload_document.html', {'form': form})

@login_required
def delete_document(request, pk):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    document = get_object_or_404(ClubDocument, pk=pk, club=club)
    document.delete()
    messages.success(request, "Document deleted successfully!")
    return redirect('club_leader:list_documents')

@login_required
def list_documents(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    documents = ClubDocument.objects.filter(club=club)
    return render(request, 'club_leader/list_documents.html', {'documents': documents})

@login_required
def create_announcement(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.club = club
            announcement.save()
            messages.success(request, "Announcement created successfully!")
            return redirect("club_leader:list_announcements")
    else:
        form = AnnouncementForm()
    return render(request, "club_leader/create_announcement.html", {"form": form})

@login_required
def list_announcements(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")

    announcements = Announcement.objects.filter(club=club).order_by("-created_at")

    context = {
        "announcements": announcements,
        "is_leader": True,  # Pass this for template logic
    }
    return render(request, "club_leader/list_announcements.html", context)

@login_required
def delete_announcement(request, pk):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    announcement = get_object_or_404(Announcement, pk=pk, club=club)
    announcement.delete()
    messages.success(request, "Announcement deleted successfully!")
    return redirect("club_leader:list_announcements")

@login_required
def edit_announcement(request, pk):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    announcement = get_object_or_404(Announcement, pk=pk, club=club)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated successfully!")
            return redirect("club_leader:list_announcements")
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, "club_leader/edit_announcement.html", {"form": form})


@login_required
def toggle_visibility(request, pk):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    announcement = get_object_or_404(Announcement, pk=pk, club=club)
    announcement.visible = not announcement.visible
    announcement.save()
    
    return JsonResponse({
        'success': True,
        'visible': announcement.visible,
    })

@login_required
def event_calendar(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    events = Event.objects.filter(club=club).order_by('event_date')
    form = EventRequestForm()
    return render(request, 'club_leader/calendar.html', {'events': events, 'form': form})

@login_required
def get_events(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    events = Event.objects.filter(club=club)
    event_list = [
        {"title": e.title, "start": e.event_date.isoformat(), "approval_status": e.approval_status}
        for e in events
    ]
    return JsonResponse(event_list, safe=False)

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    club = get_leader_club(request.user)
    if not club or event.club != club:
        return HttpResponseForbidden("You're not authorized to edit this event.")

    if request.method == "POST":
        form = EventRequestForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully! Approval required.")
            return redirect("club_leader:calendar")
    else:
        form = EventRequestForm(instance=event)

    return render(request, "club_leader/edit_event.html", {"form": form, "event": event})


@login_required
def list_upcoming_events(request):
    club = get_leader_club(request.user)
    if not club:
        return HttpResponseForbidden("You're not authorized.")
    
    events = Event.objects.filter(club=club).order_by('event_date')
    form = EventRequestForm()
    return render(request, 'club_leader/list_upcoming_events.html', {'events': events, 'form': form})

@login_required
def manage_membership_requests(request):
    memberships = Membership.objects.filter(
        club__memberships__user=request.user,
        club__memberships__membership_type='leader',
        membership_type='pending'
    ).select_related("club", "user")

    return render(request, "club_leader/manage_requests.html", {
        "requests": memberships
    })

@login_required
def update_membership_status(request, membership_id, action):
    membership = get_object_or_404(Membership, id=membership_id)

    if not membership.club.is_user_leader(request.user):
        return HttpResponseForbidden()

    if action == "approve":
        membership.membership_type = "member"
        messages.success(request, f"{membership.user.name} has been accepted.")
    elif action == "reject":
        membership.delete()
        messages.info(request, f"{membership.user.name}'s request was rejected.")
    
    membership.save()
    return redirect("club_leader:manage_requests")

@login_required
def faq_leader(request):
    # Check if the user is a leader in any club
    if not Membership.objects.filter(user=request.user, membership_type='leader').exists():
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    return render(request, 'Club_leader/faq_leader.html')
