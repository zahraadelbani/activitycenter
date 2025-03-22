from django.db import models

class Club(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    quota = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def leader(self):
        """Return the user who is the leader of the club."""
        leader_membership = self.memberships.filter(membership_type="leader").select_related("user").first()
        return leader_membership.user if leader_membership else None

    def members(self):
        """Return all users who are regular members of the club."""
        return [m.user for m in self.memberships.filter(membership_type="member").select_related("user")]

    def get_leader(self):
        """Return the Membership object for the leader."""
        return self.memberships.filter(membership_type="leader").first()

    def get_member_count(self):
        """Return the number of club members (excluding leaders/pending)."""
        return self.memberships.filter(membership_type="member").count()

    def is_user_leader(self, user):
        """Check if a given user is the leader of the club."""
        return self.memberships.filter(user=user, membership_type="leader").exists()


class Event(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    participants = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    needs = models.TextField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transportation_request = models.BooleanField(default=False)
    supporting_documents = models.FileField(upload_to='event_docs/', blank=True, null=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    approval_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rescheduled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            original_event = Event.objects.filter(pk=self.pk).first()
            if original_event:
                if original_event.approval_status != self.approval_status:
                    print(f"Status changed from {original_event.approval_status} to {self.approval_status}")
                if original_event.approval_status in ["approved", "rejected"]:
                    self.approval_status = "pending"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class RescheduleRequest(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    club_leader = models.ForeignKey('users.User', on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved')
    ], default='pending')

    def __str__(self):
        return f"Reschedule Request for {self.event.title}"


class Meeting(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="meetings")
    date_time = models.DateTimeField()
    agenda = models.TextField()

    def __str__(self):
        return f"Meeting with {self.club.name} on {self.date_time}"


class Announcement(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="announcements")
    title = models.CharField(max_length=255)
    content = models.TextField()
    visible = models.BooleanField(default=True)
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