from django import forms
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
