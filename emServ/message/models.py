from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_to')
    text_message = models.TextField()
    subject = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}->[{}|{}]'.format(self.subject, self.sender, self.to)