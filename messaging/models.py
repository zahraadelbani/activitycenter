from django.db import models
from django.conf import settings
from clubs.models import Club
from django.utils.text import slugify


class ChatRoom(models.Model):
    club = models.OneToOneField(Club, on_delete=models.CASCADE, related_name='chat_room')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Club: {self.club.name})"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.name}: {self.content[:30]}..."

class DirectChatRoom(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Chat between {self.user1.name} & {self.user2.name} "
    
    @classmethod
    def get_or_create_between_users(cls, user_a, user_b):
        user1, user2 = sorted([user_a, user_b], key=lambda u: u.id)
        room, created = cls.objects.get_or_create(user1=user1, user2=user2)
        return room, created

class DirectMessage(models.Model):
    room = models.ForeignKey(DirectChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_direct_messages", blank=True, null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_direct_messages", blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender.name} to {self.receiver.name}: {self.content[:30]}"