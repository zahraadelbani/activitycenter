from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reminders.models import EventReminder
from .models import MembershipTerminationRequest
from clubs.models import Announcement, Club, ClubDocument, Event
from feedback.models import Feedback
from users.models import User, Membership
from django.core.mail import send_mail
from django.utils import timezone
from threading import Timer
from clubs.models import Event
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@login_required
def dashboard(request):
    user = request.user

    # Clubs where the user is a member
    member_clubs = Club.objects.filter(
        memberships__user=user,
        memberships__membership_type="member"
    )

    # Exclude already joined clubs
    joined_club_ids = member_clubs.values_list("id", flat=True)

    # Only show clubs with quota and where the user hasn't exceeded club limit (max 3)
    available_clubs = [
        club for club in Club.objects.exclude(id__in=joined_club_ids)
        if club.has_quota() and Membership.objects.filter(user=user).count() < 3
    ]

    # Upcoming approved events for member clubs
    upcoming_events = Event.objects.filter(
        club__in=member_clubs,
        approval_status="approved"
    ).select_related("club").order_by("event_date")

    # Termination requests (pending only)
    termination_requests = MembershipTerminationRequest.objects.filter(
        membership__user=user,
        status="pending"
    )

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


@login_required
def event_calendar_member(request):
    clubs = Club.objects.filter(memberships__user=request.user, memberships__membership_type="member")

    if not clubs.exists():
        return HttpResponseForbidden("You're not a member of any clubs.")

    events = Event.objects.filter(club__in=clubs, approval_status="approved").select_related("club").order_by("event_date")
    reminders = EventReminder.objects.filter(user=request.user, event__in=events).values_list("event_id", flat=True)

    return render(request, "club_member/calendar.html", {
        "events": events,
        "reminders": reminders,
        "clubs": clubs,
    })

@login_required
def get_events_member(request):
    # Get all clubs the user is a member of
    clubs = Club.objects.filter(
        memberships__user=request.user,
        memberships__membership_type="member"
    )

    # If user is not part of any club, return empty list
    if not clubs.exists():
        return JsonResponse([], safe=False)

    # Fetch all approved events in those clubs
    approved_events = Event.objects.filter(
        club__in=clubs,
        approval_status="approved"
    ).select_related("club")

    # Format events for FullCalendar
    data = [
        {
            "title": f"{event.title} ({event.club.name})",
            "start": event.event_date.isoformat(),
            "approval_status": event.approval_status,
        }
        for event in approved_events
    ]

    return JsonResponse(data, safe=False)

@login_required
def remind_me(request, event_id):
    event = get_object_or_404(Event, id=event_id, approval_status="approved")

    if request.method == "POST":
        user = request.user

        # Check if reminder already exists
        if EventReminder.objects.filter(user=user, event=event).exists():
            messages.warning(request, "You’ve already requested a reminder for this event.")
            return redirect("club_member:event_calendar")

        scheduled_for = timezone.now() + timezone.timedelta(minutes=1)  # testing

        # Save the reminder
        EventReminder.objects.create(
            user=user,
            event=event,
            scheduled_for=scheduled_for,
        )

        # Send reminder function
        def send_reminder():
            subject = f"Reminder: {event.title}"
            from_email = "no-reply@activitycenter.com"
            to = [user.email]

            # Plain text version
            text_content = (
                f"Hello {user.name},\n\n"
                f"{event.title} is happening on {event.event_date.strftime('%A, %B %d at %I:%M %p')}.\n\n"
                f"Club: {event.club.name}\n"
                f"Created by: {event.created_by.name if event.created_by else 'N/A'}\n\n"
                f"- Activity Center"
            )

            # HTML version with image
            image_url = request.build_absolute_uri(event.image.url) if event.image else None 


            html_content = render_to_string("emails/event_reminder.html", {
                "user": user,
                "event": event,
                "image_url": image_url,
            })

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        # Send email after delay (for testing)
        Timer(60, send_reminder).start()

        messages.success(request, f"You’ll be reminded about \"{event.title}\" in 1 minute.")
        return redirect("club_member:event_calendar")

@login_required
def member_announcements(request):
    user = request.user

    # All clubs the user is a member of
    user_clubs = Club.objects.filter(memberships__user=user, memberships__membership_type="member")

    # Apply filter if selected
    selected_club_id = request.GET.get("club")
    if selected_club_id:
        announcements = Announcement.objects.filter(
            club__in=user_clubs, club__id=selected_club_id, visible=True
        ).order_by("-created_at")
    else:
        announcements = Announcement.objects.filter(
            club__in=user_clubs, visible=True
        ).order_by("-created_at")

    return render(request, "club_member/member_announcements.html", {
        "announcements": announcements,
        "user_clubs": user_clubs
    })