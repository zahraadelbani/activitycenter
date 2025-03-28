from django import forms
from .models import Candidate, Position
from users.models import Membership

class SelfNominationForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["position", "manifesto"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["position"].queryset = Position.objects.none()

class VotingForm(forms.Form):
    def __init__(self, *args, election=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        user_clubs = Membership.objects.filter(
            user=user, membership_type="member"
        ).values_list("club_id", flat=True)

        position_club_pairs = Candidate.objects.filter(
            election=election,
            approved=True,
            club__id__in=user_clubs
        ).values_list(
            "position__id",
            "position__name",
            "club__id",
            "club__name"
        ).distinct()

        for (pos_id, pos_name, club_id, club_name) in position_club_pairs:
            field_label = f"{pos_name} ({club_name})"
            candidates = Candidate.objects.filter(
                election=election,
                approved=True,
                position__id=pos_id,
                club__id=club_id
            )

            field = forms.ModelChoiceField(
                queryset=candidates,
                label=field_label,
                widget=forms.RadioSelect,
                required=True
            )

            def candidate_label(obj):
                return f"{obj.user.name} - {obj.position.name} ({obj.club.name})"
            field.label_from_instance = candidate_label

            field_name = f"pos{pos_id}_club{club_id}"
            self.fields[field_name] = field
