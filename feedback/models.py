from django.db import models
from users.models import User
from clubs.models import Club

class ClubFeedback(models.Model):
    club_member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedback_given")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="feedback_received")
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.club_member.name} to {self.club.name}"
