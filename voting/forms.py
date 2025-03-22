from django import forms
from .models import Candidate, Position

class SelfNominationForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["position", "manifesto"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields["position"].queryset = Position.objects.filter(election__is_active=True)
        
    def save(self, commit=True, user=None):
        candidate = super().save(commit=False)
        candidate.user = user
        candidate.election = candidate.position.election  # ✅ this fixes the IntegrityError
        candidate.self_nominated = True
        candidate.approved = False
        if commit:
            candidate.save()
        return candidate
