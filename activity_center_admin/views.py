from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
# from django.contrib.auth.decorators import login_required  # Temporarily removed
# from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

# from club_management.decorators import role_required  # Temporarily removed
from clubs.models import Club, Meeting, Event
#from events.models import Event  # Ensure you have an Event model in events/models.py
from clubs.models import Announcement  # ✅ Correct import
#from events.forms import EventForm

# --- Dashboard ---
# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class DashboardView(TemplateView):
    template_name = 'activity_center_admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clubs'] = Club.objects.all()
        context['pending_activities'] = Event.objects.filter(approval_status='pending')
        context['pending_announcements'] = Announcement.objects.filter(status='pending')
        return context

# --- Clubs CRUD ---
# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class ClubListView(ListView):
    model = Club
    template_name = 'activity_center_admin/club_list.html'
    context_object_name = 'clubs'

# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class ClubCreateView(CreateView):
    model = Club
    fields = ['name', 'description', 'leader', 'members', 'quota']
    template_name = 'activity_center_admin/club_form.html'
    success_url = reverse_lazy('activity_center_admin:club_list')

    def form_valid(self, form):
        messages.success(self.request, "Club created successfully.")
        return super().form_valid(form)

# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class ClubUpdateView(UpdateView):
    model = Club
    fields = ['name', 'description', 'leader', 'members', 'quota']
    template_name = 'activity_center_admin/club_form.html'
    success_url = reverse_lazy('activity_center_admin:club_list')

    def form_valid(self, form):
        messages.success(self.request, "Club updated successfully.")
        return super().form_valid(form)

# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class ClubDeleteView(DeleteView):
    model = Club
    template_name = 'activity_center_admin/club_confirm_delete.html'
    success_url = reverse_lazy('activity_center_admin:club_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Club deleted successfully.")
        return super().delete(request, *args, **kwargs)

# --- Events CRUD ---
# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class EventListView(ListView):
    model = Event
    template_name = 'activity_center_admin/event_list.html'
    context_object_name = 'events'

# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class EventCreateView(CreateView):
    model = Event
    #form_class = EventForm  # Use the custom form with a date picker
    template_name = 'activity_center_admin/event_form.html'
    success_url = reverse_lazy('activity_center_admin:event_list')

    def form_valid(self, form):
        messages.success(self.request, "Event created successfully.")
        return super().form_valid(form)

# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class EventUpdateView(UpdateView):
    model = Event
    #form_class = EventForm  # Use the custom form with a date picker
    template_name = 'activity_center_admin/event_form.html'
    success_url = reverse_lazy('activity_center_admin:event_list')

    def form_valid(self, form):
        messages.success(self.request, "Event updated successfully.")
        return super().form_valid(form)

# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'activity_center_admin/event_confirm_delete.html'
    success_url = reverse_lazy('activity_center_admin:event_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Event deleted successfully.")
        return super().delete(request, *args, **kwargs)

# --- Club Activities Actions ---
# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class ActivityListView(ListView):
    model = Event
    template_name = 'activity_center_admin/activity_list.html'
    context_object_name = 'activities'

# @login_required
# @role_required('Activity Center Admin')
def activity_approve(request, activity_id):
    activity = get_object_or_404(Event, id=activity_id)
    activity.status = 'approved'
    activity.save()
    messages.success(request, "Activity approved.")
    return redirect('activity_center_admin:activity_list')

# @login_required
# @role_required('Activity Center Admin')
def activity_reject(request, activity_id):
    activity = get_object_or_404(Event, id=activity_id)
    activity.status = 'rejected'
    activity.save()
    messages.success(request, "Activity rejected.")
    return redirect('activity_center_admin:activity_list')

# --- Schedule Meeting for an Activity ---
# @login_required
# @role_required('Activity Center Admin')
def schedule_meeting(request, activity_id):
    activity = get_object_or_404(Event, id=activity_id)
    if request.method == 'POST':
        date_time = request.POST.get('date_time')
        agenda = request.POST.get('agenda')
        Meeting.objects.create(club=activity.club, date_time=date_time, agenda=agenda)
        messages.success(request, "Meeting scheduled successfully.")
        return redirect('activity_center_admin:activity_list')
    return render(request, 'activity_center_admin/schedule_meeting_form.html', {'activity': activity})

# --- Announcements Actions ---
# @method_decorator([login_required, role_required('Activity Center Admin')], name='dispatch')
class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'activity_center_admin/announcement_list.html'
    context_object_name = 'announcements'

# @login_required
# @role_required('Activity Center Admin')
def announcement_approve(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.status = 'approved'
    announcement.save()
    messages.success(request, "Announcement approved.")
    return redirect('activity_center_admin:announcement_list')

# @login_required
# @role_required('Activity Center Admin')
def announcement_reject(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.status = 'rejected'
    announcement.save()
    messages.success(request, "Announcement rejected.")
    return redirect('activity_center_admin:announcement_list')
