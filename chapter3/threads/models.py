from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to="thread_images", blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.content[:50]}..." if len(self.content) > 50 else self.content

    def get_absolute_url(self):
        return reverse("threads:thread-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 이미지가 있는 경우, 리사이징
        if self.image:
            img = Image.open(self.image.path)

            # 이미지가 최대 크기(800x800)를 초과하는 경우 리사이징
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)

            img.save(self.image.path)


class Comment(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]  # 오래된 댓글부터 표시

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}..."


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 한 사용자가 같은 쓰레드에 여러 개의 좋아요를 누를 수 없도록 제약 설정
        constraints = [
            models.UniqueConstraint(fields=["user", "thread"], name="unique_like")
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.thread.content[:20]}..."


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_follow"
            )
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
