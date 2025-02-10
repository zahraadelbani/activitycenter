from django import forms
from .models import Poll, Choice

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'is_active']

class ChoiceForm(forms.ModelForm):
    text = forms.CharField(required=False)  # ✅ Make this field optional

    class Meta:
        model = Choice
        fields = ['text']

class ChoiceCountForm(forms.Form):
    CHOICES_COUNT = [(i, f"{i} choices") for i in range(2, 11)]  # Dropdown for 2-10 choices
    num_choices = forms.ChoiceField(choices=CHOICES_COUNT, label="Number of Choices")
