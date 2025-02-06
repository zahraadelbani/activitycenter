from django.db import models
from users.models import User
from clubs.models import Club

class Poll(models.Model):
    """
    Represents a general poll in a club.
    Members can vote on various poll topics.
    """
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="polls")
    question = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question} - {self.club.name}"


class PollChoice(models.Model):
    """
    Represents individual choices within a poll.
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text


class PollVote(models.Model):
    """
    Tracks votes in a poll.
    Each user can vote once per poll.
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poll_votes")
    choice = models.ForeignKey(PollChoice, on_delete=models.CASCADE, related_name="poll_choice_votes")
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote by {self.voter.name} on {self.poll.question}"


class LeaderVote(models.Model):
    """
    Stores votes in club leader elections.
    Each member can vote for one leader per club election.
    """
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="leader_votes")
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes_cast")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes_received")  
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote by {self.voter.name} for {self.candidate.name} in {self.club.name}"
