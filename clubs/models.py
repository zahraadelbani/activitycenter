from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

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

class Event(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    club = models.ForeignKey('clubs.Club', on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    participants = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    needs = models.TextField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transportation_request = models.BooleanField(default=False)
    supporting_documents = models.FileField(upload_to='event_docs/', blank=True, null=True)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    approval_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rescheduled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # If the event already exists and is being updated
        if self.pk:
            # Fetch the original event status before saving
            original_event = Event.objects.filter(pk=self.pk).first()
            if original_event:
                if original_event.approval_status != self.approval_status:
                    print(f"Status changed from {original_event.approval_status} to {self.approval_status}")

                # If it's being edited by the club leader, reset to pending
                if original_event.approval_status == "approved" or original_event.approval_status == "rejected":
                    self.approval_status = "pending"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class RescheduleRequest(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    club_leader = models.ForeignKey('users.ClubLeader', on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')

    def __str__(self):
        return f"Reschedule Request for {self.event.title}"

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
    visible = models.BooleanField(default=True)  # ✅ Visibility toggle (default: visible to members)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({'Visible' if self.visible else 'Hidden'})"

class ClubDocument(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="club_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.club.name})"