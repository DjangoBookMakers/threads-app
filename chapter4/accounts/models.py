from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )
    website = models.URLField(max_length=200, blank=True)
    following = models.ManyToManyField(
        "self", through="Follow", related_name="followers", symmetrical=False
    )

    def __str__(self):
        return self.username

    def get_followers_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.following.count()


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name="following_relationships", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="follower_relationships", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
