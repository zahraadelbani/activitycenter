""" from django import forms
from django.utils import timezone
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'club']
        widgets = {
            'event_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event_date'].input_formats = ['%Y-%m-%dT%H:%M']
        # If updating an existing instance, convert the datetime to local time
        if self.instance and self.instance.pk and self.instance.event_date:
            # Convert the event_date to local time if it's timezone-aware
            local_dt = timezone.localtime(self.instance.event_date)
            self.initial['event_date'] = local_dt.strftime('%Y-%m-%dT%H:%M') """


from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
