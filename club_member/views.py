from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MembershipTerminationRequest
from clubs.models import Club, ClubDocument, Event
from feedback.models import Feedback
from users.models import User, Membership

@login_required
def dashboard(request):
    user = request.user
    member_clubs = Club.objects.filter(memberships__user=user, memberships__membership_type="member")
    joined_club_ids = member_clubs.values_list("id", flat=True)
    available_clubs = [club for club in Club.objects.exclude(id__in=joined_club_ids) if club.has_quota() and Membership.objects.filter(user=user).count() < 3]
    upcoming_events = Event.objects.filter(club__in=member_clubs).order_by("event_date")
    termination_requests = MembershipTerminationRequest.objects.filter(membership__user=user, status="pending")

    context = {
        "member_clubs": member_clubs,
        "upcoming_events": upcoming_events,
        "termination_requests": termination_requests,
        "available_clubs": available_clubs,
    }
    return render(request, "club_member/dashboard.html", context)

@login_required
def join_club(request):
    user = request.user
    total_memberships = Membership.objects.filter(user=user).count()

    if request.method == "POST":
        club_id = request.POST.get("club_id")
        club = get_object_or_404(Club, id=club_id)

        if Membership.objects.filter(user=user, club=club).exists():
            messages.error(request, "You already have a membership (of any type) with this club.")
            return redirect("club_member:dashboard")

        if total_memberships >= 3:
            messages.error(request, "You cannot have more than 3 total memberships (including pending ones).")
            return redirect("club_member:dashboard")

        if not club.has_quota():
            messages.error(request, "This club has reached its member quota.")
            return redirect("club_member:dashboard")

        Membership.objects.create(user=user, club=club, membership_type="member")
        messages.success(request, f"You have successfully joined {club.name}.")

    return redirect("club_member:dashboard")

@login_required
def leave_club(request, club_id):
    user = request.user
    membership = get_object_or_404(Membership, user=user, club_id=club_id, membership_type="member")

    existing_request = MembershipTerminationRequest.objects.filter(membership=membership, status="pending").exists()

    if existing_request:
        messages.error(request, "You already have a pending request to leave this club.")
    else:
        MembershipTerminationRequest.objects.create(membership=membership, club=membership.club)
        messages.success(request, "Your request to leave has been submitted.")

    return redirect("club_member:dashboard")

@login_required
def view_documents(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    documents = ClubDocument.objects.filter(club=club)
    return render(request, "club_member/documents.html", {"club": club, "documents": documents})

@login_required
def view_events(request):
    user = request.user
    member_clubs = Club.objects.filter(memberships__user=user, memberships__membership_type="member")
    events = Event.objects.filter(club__in=member_clubs).order_by("event_date")
    return render(request, "club_member/events.html", {"events": events})

@login_required
def cancel_termination_request(request, request_id):
    termination_request = get_object_or_404(MembershipTerminationRequest, id=request_id, membership__user=request.user)

    if termination_request.status == "pending":
        termination_request.delete()
        messages.success(request, "Your membership termination request has been canceled.")
    else:
        messages.error(request, "You can only cancel pending termination requests.")

    return redirect("club_member:dashboard")
