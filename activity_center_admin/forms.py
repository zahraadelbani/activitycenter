from django import forms
from voting.models import Election

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = [
            "name", 
            "start_date", "end_date",
            "nomination_start", "nomination_end",
            "is_active"
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'nomination_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'nomination_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
