# Refactored polls/forms.py
from django import forms
from .models import Poll, Choice

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["question"]


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["text"]

class ChoiceCountForm(forms.Form):
    num_choices = forms.IntegerField(
        label="Number of Choices",
        min_value=2,
        max_value=10,
        help_text="Enter how many choices this poll should have (between 2 and 10)."
    )