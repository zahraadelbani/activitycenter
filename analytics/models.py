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

    def members_percentage(self):
        """Calculate percentage of members based on club quota."""
        if self.club.quota > 0:
            return round((self.total_members / self.club.quota) * 100, 2)
        return 0  # Avoid division by zero

    def __str__(self):
        return f"Analytics for {self.club.name}"

