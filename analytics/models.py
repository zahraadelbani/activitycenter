from django.db import models
from clubs.models import Club

class ClubAnalytics(models.Model):
    """Stores analytics for a club."""
    club = models.OneToOneField(Club, on_delete=models.CASCADE, related_name="analytics")
    total_members = models.PositiveIntegerField(default=0)
    total_events = models.PositiveIntegerField(default=0)
    total_polls = models.PositiveIntegerField(default=0)

    def update_stats(self):
        """Recalculate analytics data."""
        self.total_members = self.club.memberships.count()
        self.total_events = self.club.events.count()
        self.total_polls = self.club.polls.count()
        self.save()

    def __str__(self):
        return f"Analytics for {self.club.name}"
