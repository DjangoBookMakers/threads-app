import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User


@receiver(post_delete, sender=User)
def auto_delete_profile_image_on_delete(sender, instance, **kwargs):
    """
    사용자가 삭제될 때 프로필 이미지 파일 삭제
    """
    if instance.profile_image:
        if os.path.isfile(instance.profile_image.path):
            os.remove(instance.profile_image.path)
