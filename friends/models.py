from django.db import models
from django.contrib.auth import get_user_model

class Friendship(models.Model):
    PENDING = 'P'
    ACCEPTED = 'A'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
    ]

    user = models.ForeignKey(get_user_model(), related_name='sent_requests', on_delete=models.CASCADE)
    friend = models.ForeignKey(get_user_model(), related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=1)

    def __str__(self):
        return f"{self.user.username} and {self.friend.username} - {self.get_status_display()}"
