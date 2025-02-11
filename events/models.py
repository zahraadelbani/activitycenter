from django.db import models
from clubs.models import Club
from users.models import ClubLeader

class Event(models.Model):
    club = models.ForeignKey(
        Club, 
        on_delete=models.CASCADE, 
        related_name="events"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="event_images/", blank=True, null=True)
    created_by = models.ForeignKey(
        ClubLeader, 
        on_delete=models.CASCADE, 
        related_name="created_events"
    )

    def __str__(self):
        return f"{self.title} - {self.club.name}"
