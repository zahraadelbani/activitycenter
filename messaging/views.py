from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatRoom, Message, DirectChatRoom, DirectMessage
from polls.models import Poll, Choice, PollVote
from clubs.models import Club
from users.models import Membership
from collections import defaultdict

@login_required
def group_chat(request, room_slug):
    room = get_object_or_404(ChatRoom, slug=room_slug)
    messages_qs = Message.objects.filter(room=room).order_by("timestamp")

    # Ensure user is a member or leader of this club
    membership = Membership.objects.filter(
        user=request.user,
        club=room.club,
        membership_type__in=["member", "leader"]
    ).first()

    if not membership:
        messages.error(request, "You are not a member of this club.")
        return redirect("home")

    polls = Poll.objects.filter(club=room.club, is_active=True).order_by("-created_at")

    # Handle POST actions
    if request.method == "POST":
        if "create_poll" in request.POST:
            if membership.membership_type == "leader":
                question = request.POST.get("question")
                choices = request.POST.getlist("choices[]")
                if question and choices:
                    poll = Poll.objects.create(
                        club=room.club,
                        question=question,
                        created_by=request.user,
                        is_active=True,
                    )
                    for choice_text in choices:
                        if choice_text.strip():
                            Choice.objects.create(poll=poll, text=choice_text.strip())
                    messages.success(request, "Poll created successfully.")
                    return redirect("messaging:group_chat", room_slug=room.slug)
                else:
                    messages.error(request, "Poll question and choices are required.")

        elif "vote_poll" in request.POST:
            poll_id = request.POST.get("poll_id")
            choice_id = request.POST.get("choice_id")
            poll = get_object_or_404(Poll, id=poll_id, club=room.club)
            choice = get_object_or_404(Choice, id=choice_id, poll=poll)

            already_voted = PollVote.objects.filter(poll=poll, user=request.user).exists()
            if not already_voted:
                PollVote.objects.create(poll=poll, choice=choice, user=request.user)
                messages.success(request, "Vote submitted successfully.")
            else:
                messages.warning(request, "You have already voted on this poll.")

            return redirect("messaging:group_chat", room_slug=room.slug)

   # Precompute vote status and selected choice
    polls_with_vote_status = []
    for poll in polls:
        vote = PollVote.objects.filter(user=request.user, poll=poll).first()
        has_voted = vote is not None
        selected_choice_id = vote.choice.id if vote else None
        polls_with_vote_status.append((poll, has_voted, selected_choice_id))

    return render(request, "messaging/group_chat.html", {
        "room": room,
        "club": room.club,
        "messages": messages_qs,
        "polls_with_vote_status": polls_with_vote_status,
        "membership": membership,
        "room_slug": room.slug, 
    })


@login_required
def messaging_rooms(request):
    user = request.user

    # Get all clubs the user is part of (member or leader)
    clubs = Club.objects.filter(memberships__user=user, memberships__membership_type__in=["member", "leader"])
    chat_rooms = ChatRoom.objects.filter(club__in=clubs)

    # Users in same clubs for DMs
    users_in_same_clubs = set()
    user_club_map = {}
    for club in clubs:
        members = Membership.objects.filter(
            club=club,
            membership_type__in=["member", "leader"]
        ).exclude(user=user)

        for member in members:
            users_in_same_clubs.add(member.user)
            user_club_map.setdefault(member.user.id, set()).add(club.name)

    # 🛠️ Join set into comma-separated string
    for user_id, club_names in user_club_map.items():
        user_club_map[user_id] = ", ".join(club_names)

    return render(request, "messaging/messaging_rooms.html", {
        "chat_rooms": chat_rooms,
        "dm_users": users_in_same_clubs,
        "user_club_map": user_club_map,
    
    })

@login_required
def direct_chat_room(request, user_id):
    # Check shared membership (same logic as group chat)
    shared_membership = Membership.objects.filter(
        user__id=user_id,
        club__in=Membership.objects.filter(user=request.user).values("club"),
        membership_type__in=["member", "leader"]
    ).select_related("user").first()

    if not shared_membership:
        return render(request, "messaging/access_denied.html")

    other_user = shared_membership.user

    # Create or get chat room
    room, created = DirectChatRoom.get_or_create_between_users(request.user, other_user)
    messages = DirectMessage.objects.filter(room=room).order_by("timestamp")

    return render(request, "messaging/direct_chat_room.html", {
        "room": room,
        "other_user": other_user,
        "messages": messages,
    })