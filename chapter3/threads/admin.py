from django.contrib import admin
from .models import Thread, Comment, Like, Follow


class ThreadAdmin(admin.ModelAdmin):
    list_display = ("content_preview", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("content", "user__username")
    date_hierarchy = "created_at"

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "내용"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("content_preview", "user", "thread_preview", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("content", "user__username", "thread__content")

    def content_preview(self, obj):
        return obj.content[:30] + "..." if len(obj.content) > 30 else obj.content

    content_preview.short_description = "내용"

    def thread_preview(self, obj):
        return (
            obj.thread.content[:30] + "..."
            if len(obj.thread.content) > 30
            else obj.thread.content
        )

    thread_preview.short_description = "쓰레드"


class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "thread_preview", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "thread__content")

    def thread_preview(self, obj):
        return (
            obj.thread.content[:30] + "..."
            if len(obj.thread.content) > 30
            else obj.thread.content
        )

    thread_preview.short_description = "쓰레드"


class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at")
    list_filter = ("created_at",)
    search_fields = ("follower__username", "following__username")


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)
