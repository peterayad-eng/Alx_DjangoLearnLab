from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Notification(models.Model):
    # Who receives the notification
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    # Who performed the action
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    # The action verb (e.g., 'liked', 'commented', 'followed')
    verb = models.CharField(max_length=255)
    # When the notification was created
    timestamp = models.DateTimeField(auto_now_add=True)
    # Whether the notification has been read
    is_read = models.BooleanField(default=False)

    # Generic foreign key for the target object (post, comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor.username} {self.verb} - {self.recipient.username}"

