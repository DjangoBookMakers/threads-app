import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Thread


@receiver(post_delete, sender=Thread)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    스레드가 삭제될 때 관련 이미지 파일 삭제
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
