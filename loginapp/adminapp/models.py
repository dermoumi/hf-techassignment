from django.db import models
from mainapp.models import User

class Notification(models.Model):
    kind = models.CharField(max_length=100, blank=True)
    content = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    users = models.ManyToManyField(User, through='UserNotification')
    time = models.DateTimeField(auto_now_add=True)

    def natural_key(self):
        return {
            'kind': self.kind,
            'content': self.content,
            'link': self.link
        }

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    unread = models.BooleanField(default=True)
