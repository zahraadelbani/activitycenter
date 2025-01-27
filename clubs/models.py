from django.db import models
from django.contrib.auth.models import User

from users.models import ClubLeader
class Club(models.Model):
    id = models.AutoField(primary_key=True)  # Add ID as primary key
    name = models.CharField(max_length=255)
    description = models.TextField()
    quota = models.PositiveIntegerField(default=0)  # Add quota field
    leader = models.OneToOneField(
        ClubLeader,
        on_delete=models.SET_NULL,
        null=True,  # Allow null in the database
        blank=True,  # Allow blank in forms
        related_name='club'
    )  # Optional relationship with ClubLeader
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ClubActivity(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"


class Meeting(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='meetings')
    date_time = models.DateTimeField()
    agenda = models.TextField()

    def __str__(self):
        return f"Meeting with {self.club.name} on {self.date_time}"


class Announcement(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
