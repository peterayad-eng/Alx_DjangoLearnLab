from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following',
        blank=True)

    def __str__(self):
        return self.username

    def follow_user(self, user_to_follow):
        """Makes this user follow another user."""
        if user_to_follow != self:
            self.followers.add(user_to_follow)

    def unfollow_user(self, user_to_unfollow):
        """Makes this user unfollow another user."""
        self.followers.remove(user_to_unfollow)

    def is_following(self, user):
        """Checks if this user is following another user."""
        return self.followers.filter(pk=user.pk).exists()

