from django.db import models
from django.conf import settings
from clubs.models import Event

class EventReminder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_reminders')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders')
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"Reminder for {self.user} - {self.event}"
