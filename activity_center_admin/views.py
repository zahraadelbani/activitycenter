from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from activity_center_admin.forms import ElectionForm
from clubs.models import Club, Meeting, Event, Announcement
from voting.models import Candidate, Election

# --- Helpers ---
def is_aca(user):
    return user.is_authenticated and user.get_role() == "activity_center_admin"

# --- Dashboard ---
@login_required
@user_passes_test(is_aca)
def activity_admin_dashboard(request):
    context = {
        'clubs': Club.objects.all(),
        'pending_activities': Event.objects.filter(approval_status='pending'),
        'pending_announcements': Announcement.objects.filter(visible=False),
        'pending_nominations': Candidate.objects.filter(self_nominated=True, approved=False).count(),
    }
    return render(request, "activity_center_admin/dashboard.html", context)

# --- Clubs CRUD ---
class ClubListView(ListView):
    model = Club
    template_name = 'activity_center_admin/club_list.html'
    context_object_name = 'clubs'

class ClubCreateView(CreateView):
    model = Club
    fields = ['name', 'description', 'quota']
    template_name = 'activity_center_admin/club_form.html'
    success_url = reverse_lazy('activity_center_admin:club_list')

    def form_valid(self, form):
        messages.success(self.request, "Club created successfully.")
        return super().form_valid(form)

class ClubUpdateView(UpdateView):
    model = Club
    fields = ['name', 'description', 'quota']
    template_name = 'activity_center_admin/club_form.html'
    success_url = reverse_lazy('activity_center_admin:club_list')

    def form_valid(self, form):
        messages.success(self.request, "Club updated successfully.")
        return super().form_valid(form)

class ClubDeleteView(DeleteView):
    model = Club
    template_name = 'activity_center_admin/club_confirm_delete.html'
    success_url = reverse_lazy('activity_center_admin:club_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Club deleted successfully.")
        return super().delete(request, *args, **kwargs)

# --- Events CRUD & Approval ---
class EventListView(ListView):
    model = Event
    template_name = 'activity_center_admin/event_list.html'
    context_object_name = 'events'

class EventCreateView(CreateView):
    model = Event
    fields = ['club', 'title', 'event_date', 'participants', 'image', 'needs', 'total_cost', 'transportation_request', 'supporting_documents']
    template_name = 'activity_center_admin/event_form.html'
    success_url = reverse_lazy('activity_center_admin:event_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Event created successfully.")
        return super().form_valid(form)

class EventUpdateView(UpdateView):
    model = Event
    fields = ['club', 'title', 'event_date', 'participants', 'image', 'needs', 'total_cost', 'transportation_request', 'supporting_documents']
    template_name = 'activity_center_admin/event_form.html'
    success_url = reverse_lazy('activity_center_admin:event_list')

    def form_valid(self, form):
        messages.success(self.request, "Event updated successfully.")
        return super().form_valid(form)

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'activity_center_admin/event_confirm_delete.html'
    success_url = reverse_lazy('activity_center_admin:event_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Event deleted successfully.")
        return super().delete(request, *args, **kwargs)

@login_required
@user_passes_test(is_aca)
def event_approve(request, activity_id):
    activity = get_object_or_404(Event, id=activity_id)
    activity.approval_status = 'approved'
    activity.save()
    messages.success(request, "Event approved.")
    return redirect('activity_center_admin:event_list')

@login_required
@user_passes_test(is_aca)
def event_reject(request, activity_id):
    activity = get_object_or_404(Event, id=activity_id)
    activity.approval_status = 'rejected'
    activity.save()
    messages.success(request, "Event rejected.")
    return redirect('activity_center_admin:event_list')

@login_required
@user_passes_test(is_aca)
def schedule_meeting(request, activity_id):
    activity = get_object_or_404(Event, id=activity_id)
    if request.method == 'POST':
        date_time = request.POST.get('date_time')
        agenda = request.POST.get('agenda')
        Meeting.objects.create(club=activity.club, date_time=date_time, agenda=agenda)
        messages.success(request, "Meeting scheduled successfully.")
        return redirect('activity_center_admin:event_list')
    return render(request, 'activity_center_admin/schedule_meeting_form.html', {'activity': activity})

# --- Announcements Actions ---
class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'activity_center_admin/announcement_list.html'
    context_object_name = 'announcements'

@login_required
@user_passes_test(is_aca)
def announcement_approve(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.visible = True
    announcement.save()
    messages.success(request, "Announcement approved.")
    return redirect('activity_center_admin:announcement_list')

@login_required
@user_passes_test(is_aca)
def announcement_reject(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.visible = False
    announcement.save()
    messages.success(request, "Announcement rejected.")
    return redirect('activity_center_admin:announcement_list')

# --- Nomination Management ---
@login_required
@user_passes_test(is_aca)
def manage_nominations(request):
    pending_candidates = Candidate.objects.filter(self_nominated=True, approved=False)
    return render(request, "activity_center_admin/manage_nominations.html", {
        "pending_candidates": pending_candidates,
    })

@login_required
@user_passes_test(is_aca)
def approve_nomination(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id, self_nominated=True)
    candidate.approved = True
    candidate.save()
    messages.success(request, f"Approved nomination for {candidate.user.name}.")
    return redirect("activity_center_admin:manage_nominations")

@login_required
@user_passes_test(is_aca)
def reject_nomination(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id, self_nominated=True)
    candidate.delete()
    messages.warning(request, f"Rejected nomination for {candidate.user.name}.")
    return redirect("activity_center_admin:manage_nominations")

# --- Election Management ---
@login_required
@user_passes_test(is_aca)
def manage_elections(request):
    elections = Election.objects.all().order_by("-start_date")
    return render(request, "activity_center_admin/manage_elections.html", {"elections": elections})

@login_required
@user_passes_test(is_aca)
def create_election(request):
    if request.method == "POST":
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New election created!")
            return redirect("activity_center_admin:manage_elections")
    else:
        form = ElectionForm()

    return render(request, "activity_center_admin/create_election.html", {"form": form})

@login_required
@user_passes_test(is_aca)
def edit_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    if request.method == "POST":
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, "Election updated!")
            return redirect("activity_center_admin:manage_elections")
    else:
        form = ElectionForm(instance=election)

    return render(request, "activity_center_admin/edit_election.html", {
        "election": election,
        "form": form,
    })

@login_required
@user_passes_test(is_aca)
def delete_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    if request.method == "POST":
        election.delete()
        messages.success(request, "Election deleted.")
        return redirect("activity_center_admin:manage_elections")
    return redirect("activity_center_admin:manage_elections")

from django.utils.timezone import now as timezone_now
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from voting.models import Election

@login_required
@user_passes_test(is_aca)
def manage_elections(request):
    elections = Election.objects.all().order_by("-start_date")
    current_time = timezone_now()

    for e in elections:
        # Skip if any critical date is missing
        if not e.nomination_start or not e.nomination_end or not e.start_date or not e.end_date:
            e.status = "Missing Dates"
            e.status_color = "bg-red-100 text-red-800"
            continue

        if current_time < e.nomination_start:
            e.status = "Upcoming"
            e.status_color = "bg-gray-200 text-gray-800"
        elif e.nomination_start <= current_time <= e.end_date:
            e.status = "Ongoing"
            e.status_color = "bg-yellow-100 text-yellow-800"
        else:
            e.status = "Ended"
            e.status_color = "bg-green-100 text-green-800"

    return render(request, "activity_center_admin/manage_elections.html", {
        "elections": elections
    })

# activity_center_admin/views.py

@login_required
@user_passes_test(is_aca)
def toggle_election_active(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    election.is_active = not election.is_active
    election.save()
    messages.success(request, f"Election '{election.name}' is now {'active' if election.is_active else 'inactive'}.")
    return redirect("activity_center_admin:manage_elections")
