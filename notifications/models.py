from django.db import models
from users.models import User  # [SENU]: assuming you have a User model here

class Notification(models.Model):

    # id is auto added

    # link to the user who receives the notification
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    # notification type
    notification_type = models.CharField(max_length=50)  # e.g., 'message', 'alert', 'reminder', etc.
    message = models.TextField()
    data = models.JSONField(blank=True, null=True ) # extra data

    # tracking
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

