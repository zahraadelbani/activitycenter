from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet
from django.utils import timezone

cipher_suite = Fernet(settings.SECRET_ENCRYPTION_KEY.encode())

class Election(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    results_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def has_ended(self):
        return timezone.now() > self.end_date

    def has_started(self):
        return timezone.now() >= self.start_date

    @classmethod
    def get_current_election(cls):
        now = timezone.now()
        return cls.objects.filter(start_date__year=now.year, start_date__month=9, is_active=True).first()

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="positions")

    def __str__(self):
        return f"{self.name} ({self.election.name})"

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="candidates")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="candidates")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    manifesto = models.TextField(blank=True, null=True)
    votes = models.IntegerField(default=0)
    self_nominated = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.position.name}"

class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="votes")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="candidate_votes")
    encrypted_candidate = models.BinaryField(editable=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("election", "voter", "position")

    def save(self, *args, **kwargs):
        if self.candidate:
            self.encrypted_candidate = cipher_suite.encrypt(self.candidate.user.name.encode())
        super().save(*args, **kwargs)

    def get_decrypted_candidate(self):
        return cipher_suite.decrypt(self.encrypted_candidate).decode() if self.encrypted_candidate else None
