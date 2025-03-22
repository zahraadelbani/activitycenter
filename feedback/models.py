from django.db import models
from clubs.models import Club
from users.models import User

class Feedback(models.Model):
    """Stores feedback and complaints from club members."""
    
    CATEGORY_CHOICES = [
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="feedbacks")
    # Will be set to None automatically if it's a complaint
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('reviewed', 'Reviewed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_anonymous(self):
        return self.category == 'complaint'

    def display_user(self):
        return self.submitted_by.name if self.submitted_by and not self.is_anonymous() else "Anonymous"

    def save(self, *args, **kwargs):
        # Automatically anonymize complaints
        if self.category == 'complaint':
            self.submitted_by = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.title()} - {self.display_user()}"
