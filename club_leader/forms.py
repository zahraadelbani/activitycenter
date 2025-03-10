from django import forms
from clubs.models import Announcement,ClubDocument
from bootstrap_datepicker_plus.widgets import DatePickerInput
from clubs.models import Event

class EventRequestForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'event_date', 'participants', 'image', 'needs', 
            'total_cost', 'transportation_request', 'supporting_documents'
        ] 

        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'participants': forms.Textarea(attrs={'rows': 3}),
            'needs': forms.Textarea(attrs={'rows': 5}),
        }

    def save(self, commit=True):
        event = super().save(commit=False)
        if event.pk:  # If the event already exists, reset approval status
            event.approval_status = 'pending'
        if commit:
            event.save()
        return event



class ClubDocumentForm(forms.ModelForm):
    class Meta:
        model = ClubDocument
        fields = ['title', 'file']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "content", "visible"]  # ✅ Allow leaders to set visibility
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
        }
