from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class NotificationModel(models.Model):

    NOTIFICATION_TYPES = [
        (1, 'Message'),
        (2, 'Suppression'),
        (3, 'Ajout'),
    ]

    sender = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notif_sender')
    to = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notif_to')
    message = models.TextField()
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.notification_type, self.sender)