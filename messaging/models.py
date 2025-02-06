from django.db import models
from users.models import User
from clubs.models import Club

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_received", null=True, blank=True)  # Private chat
    receiver_group = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="group_messages", null=True, blank=True)  # Group chat
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.name} to {self.receiver.name if self.receiver else self.receiver_group.name}"
