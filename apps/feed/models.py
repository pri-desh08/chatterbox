from django.db import models

from django.contrib.auth.models import User

class Chatter(models.Model):
    body = models.CharField(max_length=255)

    created_by = models.ForeignKey(User, related_name='chatters', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

class Like(models.Model):
    chat = models.ForeignKey(Chatter, related_name='likes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='liked_chatters', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)