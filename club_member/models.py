from django.db import models
from users.models import ClubMember  # ✅ Use the updated ClubMember
from clubs.models import Club  

class MembershipTerminationRequest(models.Model):
    """Stores requests from members who want to leave a club."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    club_member = models.ForeignKey(
        ClubMember, on_delete=models.CASCADE, related_name="termination_requests"
    )  # ✅ Now references `users.ClubMember`
    
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Termination Request: {self.club_member.user.name} - {self.club.name}"
