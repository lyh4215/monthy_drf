from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

User = get_user_model()

class Friend(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0, 'Pending'
        ACCEPTED = 1, 'Accepted'
    user = models.ForeignKey(User, related_name='friend_send', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_receive', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'friend'], name='unique_friend')
        ]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.user.username} > {self.friend.username}"
    
class BlockedUser(models.Model):
    blocker = models.ForeignKey(User, related_name='blocker', on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(User, related_name='blocked', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['blocker', 'blocked_user'], name='unique_blocked_user')
        ]
    
    def __str__(self):
        return f"[{self.blocker.username}] blocked [{self.blocked_user.username}]"