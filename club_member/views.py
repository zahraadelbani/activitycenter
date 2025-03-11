from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ClubMember, MembershipTerminationRequest
from clubs.models import Club, ClubDocument
from clubs.models import Event
from feedback.models import Feedback
from users.models import User


# @login_required
def dashboard(request):
    """Club Member Dashboard"""
    if not request.user or request.user.is_anonymous:
        request.user = User.objects.first()  # Assign the first user in the database

    user = request.user

    # ✅ Get clubs the user has already joined
    member_clubs = Club.objects.filter(club_members__user=user)

    # ✅ Extract **only the club IDs** for filtering available clubs
    joined_club_ids = member_clubs.values_list("id", flat=True)

    # ✅ Get clubs the user **has NOT joined yet**
    available_clubs = Club.objects.exclude(id__in=joined_club_ids)

    # ✅ Fetch upcoming events for joined clubs
    upcoming_events = Event.objects.filter(club__in=member_clubs).order_by("event_date")

    # ✅ Fetch termination requests
    termination_requests = MembershipTerminationRequest.objects.filter(
        club_member__user=user, status="pending"
    )

    context = {
        "member_clubs": member_clubs,  # Shows clubs user is a member of
        "upcoming_events": upcoming_events,
        "termination_requests": termination_requests,
        "available_clubs": available_clubs,  # ✅ Now correctly filtered
    }
    return render(request, "club_member/dashboard.html", context)


# @login_required
def join_club(request):
    """Join a club (check quota & limit of 3 clubs)"""
    user = request.user

    # ✅ Get the clubs the user has already joined
    enrolled_clubs_count = ClubMember.objects.filter(user=user).count()

    if request.method == "POST":
        club_id = request.POST.get("club_id")
        club = get_object_or_404(Club, id=club_id)

        # ✅ Ensure the user is not already a member of this club
        if ClubMember.objects.filter(user=user, club=club).exists():
            messages.error(request, "You are already a member of this club.")
            return redirect("club_member:dashboard")

        # ✅ Ensure the user is not already a member of 3 clubs
        if enrolled_clubs_count >= 3:
            messages.error(request, "You cannot join more than 3 clubs.")
            return redirect("club_member:dashboard")

        # ✅ Ensure the club has space
        if club.club_members.count() >= club.quota:
            messages.error(request, "This club has reached its limit.")
            return redirect("club_member:dashboard")

        # ✅ Create membership only if all checks pass
        ClubMember.objects.create(user=user, club=club)
        messages.success(request, f"You have successfully joined {club.name}.")

    return redirect("club_member:dashboard")


def leave_club(request, club_id):
    """Request to leave a club (needs approval)"""
    if not request.user or request.user.is_anonymous:
        request.user = User.objects.first()  # Assigns first user from database for testing
        messages.info(request, "You were assigned a test user automatically.")

    user = request.user
    club_member = get_object_or_404(ClubMember, user=user, club_id=club_id)

    existing_request = MembershipTerminationRequest.objects.filter(club_member=club_member, status="pending").exists()
    
    if existing_request:
        messages.error(request, "You already have a pending request to leave this club.")
    else:
        MembershipTerminationRequest.objects.create(club_member=club_member, club=club_member.club)
        messages.success(request, "Your request to leave has been submitted.")

    return redirect("club_member:dashboard")


# @login_required
def view_documents(request, club_id):
    """View and download club documents."""
    club = get_object_or_404(Club, id=club_id)
    documents = ClubDocument.objects.filter(club=club)
    return render(request, "club_member/documents.html", {"club": club, "documents": documents})

# @login_required
def view_events(request):
    """
    Displays a list of upcoming events for the clubs the user is a member of.
    """
    user = request.user
    member_clubs = Club.objects.filter(club_members__user=user)
    events = Event.objects.filter(club__in=member_clubs).order_by("event_date")

    return render(request, "club_member/events.html", {"events": events})

# @login_required
def cancel_termination_request(request, request_id):
    """
    Allows a club member to cancel their pending termination request.
    """
    termination_request = get_object_or_404(MembershipTerminationRequest, id=request_id, club_member__user=request.user)

    if termination_request.status == "pending":
        termination_request.delete()
        messages.success(request, "Your membership termination request has been canceled.")
    else:
        messages.error(request, "You can only cancel pending termination requests.")

    return redirect("club_member:dashboard")
