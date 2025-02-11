from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from users.models import ClubLeader
from .models import Event
from .forms import EventForm
from clubs.models import Club
@login_required
def list_events(request):
    """View all events (temporary - lists all events for testing)"""
    events = Event.objects.all()  # No role check
    return render(request, "events/list_events.html", {"events": events})

@login_required
def create_event(request):
    """Create an event (temporary - any logged-in user can create)"""
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = Club.objects.first()  # Assign first club temporarily
            event.created_by = ClubLeader.objects.first()  # Assign any available ClubLeader (temporary)
            event.save()
            return redirect("list_events")
    else:
        form = EventForm()
    
    return render(request, "events/create_event.html", {"form": form})

@login_required
def update_event(request, event_id):
    """Edit an event (temporary - no club restriction)"""
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("list_events")
    else:
        form = EventForm(instance=event)

    return render(request, "events/edit_event.html", {"form": form, "event": event})

@login_required
def delete_event(request, event_id):
    """Delete an event (temporary - no role check)"""
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event.delete()
        return redirect("list_events")

    return render(request, "events/delete_event.html", {"event": event})
