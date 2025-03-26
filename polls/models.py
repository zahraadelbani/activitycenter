from django.db import models
from django.conf import settings
from clubs.models import Club

class Poll(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="polls")
    question = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.question} ({self.club.name})"


class Choice(models.Model):
    poll = models.ForeignKey("Poll", on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.text} (Poll: {self.poll.question})"


class PollVote(models.Model):
    poll = models.ForeignKey("Poll", on_delete=models.CASCADE, related_name="poll_votes")
    choice = models.ForeignKey("Choice", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="poll_votes")
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("poll", "user")
        verbose_name = "poll Vote"
        verbose_name_plural = "poll Votes"

    def __str__(self):
        return f"{getattr(self.user, 'name', 'Unknown User')} voted for '{self.choice.text}'"
