from django import forms
from clubs.models import Announcement, ClubActivity,ClubDocument

from django import forms
from clubs.models import ClubActivity  # ✅ Correct if the model is in clubs.models
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from clubs.models import ClubActivity

class ActivityRequestForm(forms.ModelForm):
    class Meta:
        model = ClubActivity
        fields = [
            'club', 'title', 'datetime', 'participants', 'image', 'needs', 
            'total_cost', 'transportation_request', 'supporting_documents'
        ]
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # ✅ Updated for DateTime
            'participants': forms.Textarea(attrs={'rows': 3}),
            'needs': forms.Textarea(attrs={'rows': 5}),
        }


    def save(self, commit=True):
        activity = super().save(commit=False)
        activity.status = 'pending'  # Ensure default is pending
        if commit:
            activity.save()
        return activity


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
