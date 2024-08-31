from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

User = get_user_model()

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friend_send', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_receive', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted')],
                              default='pending')
    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'friend'], name='unique_friend')
        ]

    def __str__(self):
        return f"{self.user.username} > {self.friend.username}"