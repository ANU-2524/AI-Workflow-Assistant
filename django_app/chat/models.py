# django_app/chat/models.py
from django.db import models
from django.contrib.auth.models import User

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted_for = models.ManyToManyField(User, related_name="deleted_chat_messages", blank=True)
