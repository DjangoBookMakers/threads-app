from django.db import models
from django.conf import settings
from django.urls import reverse


class Thread(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads"
    )
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to="threads/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

    def get_absolute_url(self):
        return reverse("threads:detail", kwargs={"pk": self.pk})
