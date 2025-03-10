from django.db import models
from users.models import User  # ✅ Import the User model
from clubs.models import Club  # ✅ Import the Club model
#from events.models import Event


class ClubMember(models.Model):
    """
    Represents a student's membership in a club.
    - Users can join up to 3 clubs.
    - Users can request to leave a club (requires approval).
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="club_memberships"
    )
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="club_members"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.club.name}"

    def can_join_club(self, club):
        """Check if a student can join a club (max 3 clubs & check quota)."""
        if ClubMember.objects.filter(user=self.user).count() >= 3:
            return False, "You cannot join more than 3 clubs."
        if club.club_members.count() >= club.quota:
            return False, "Club quota is full."
        return True, None

    def join_club(self, club):
        """Attempt to join a club."""
        can_join, error_message = self.can_join_club(club)
        if can_join:
            ClubMember.objects.create(user=self.user, club=club)
            return True, "Successfully joined the club."
        return False, error_message

    def request_leave_club(self):
        """Request to leave a club (requires club leader approval)."""
        request, created = MembershipTerminationRequest.objects.get_or_create(
            club_member=self, club=self.club, status="pending"
        )
        return (
            "Membership termination request sent to the club leader."
            if created
            else "You already have a pending termination request."
        )


class MembershipTerminationRequest(models.Model):
    """Stores requests from members who want to leave a club."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    club_member = models.ForeignKey(
        ClubMember, on_delete=models.CASCADE, related_name="termination_requests"
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Termination Request: {self.club_member.user.name} - {self.club.name}"
