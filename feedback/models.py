from django.db import models
from clubs.models import Club
from users.models import User

class Feedback(models.Model):
    """Stores feedback and complaints from club members."""
    CATEGORY_CHOICES = [
        ('complaint', 'Complaint'),  # ✅ Complaints should be anonymous
        ('suggestion', 'Suggestion'),  # ✅ Suggestions should be linked to user
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="feedbacks")
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ Allow anonymous complaints
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('reviewed', 'Reviewed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_name = self.submitted_by.name if self.submitted_by else "Anonymous"
        return f"Feedback ({self.category}) - {user_name}"
