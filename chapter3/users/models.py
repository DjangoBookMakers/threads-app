from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 프로필 이미지 리사이징
        if self.profile_image:
            img = Image.open(self.profile_image.path)

            # 이미지가 최대 크기(300x300)를 초과하는 경우 리사이징
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """사용자가 생성되면 프로필도 함께 생성"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """사용자가 저장될 때 프로필도 함께 저장"""
    instance.profile.save()
