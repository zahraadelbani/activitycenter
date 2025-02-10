from django.db import models
from django.contrib.auth.models import AbstractUser

class Club(models.Model):
    id = models.AutoField(primary_key=True)  # Add ID as primary key
    name = models.CharField(max_length=255)
    description = models.TextField()
    quota = models.PositiveIntegerField(default=0)  # Add quota field
    leader = models.OneToOneField(
        "users.ClubLeader",
        on_delete=models.SET_NULL,
        null=True,  # Allow null in the database
        blank=True,  # Allow blank in forms
        related_name='led_club'
    )  # Optional relationship with ClubLeader
    members = models.ManyToManyField('users.ClubMember', blank=True, related_name='club_memberships')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ClubActivity(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="activities")
    title = models.CharField(max_length=255)  # Subject of Activity
    datetime = models.DateTimeField()  # ✅ Changed from DateField to DateTimeField
    participants = models.TextField()  # Names of Participants
    image = models.ImageField(upload_to="activity_images/", blank=True, null=True)  # Image Upload
    needs = models.TextField()  # List of needs (parsed JSON or plain text)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total Cost
    transportation_request = models.BooleanField(default=False)  # Transport Request
    approval_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    supporting_documents = models.FileField(upload_to="activity_documents/", blank=True, null=True)  # File Attachments

    def __str__(self):
        return f"{self.title} ({self.approval_status})"


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

class ClubDocument(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="club_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.club.name})"