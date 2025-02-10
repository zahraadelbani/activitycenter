from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # Add default value
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
