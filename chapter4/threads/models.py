from django.db import models
from django.conf import settings
from django.urls import reverse
import uuid
import os


def get_file_path(instance, filename):
    """안전한 파일 경로 생성"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("threads", filename)


class Thread(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads"
    )
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

    def get_absolute_url(self):
        return reverse("threads:detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"

    def get_comment_count(self):
        return self.comments.count()

    def get_latest_comments(self, limit=2):
        return self.comments.all()[:limit]
