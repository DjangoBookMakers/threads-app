from django.contrib import admin
from .models import Thread, Comment


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "content_preview", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content", "author__username")
    date_hierarchy = "created_at"

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "내용 미리보기"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "thread", "content_preview", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content", "author__username")

    def content_preview(self, obj):
        return obj.content[:30] + "..." if len(obj.content) > 30 else obj.content

    content_preview.short_description = "내용 미리보기"
