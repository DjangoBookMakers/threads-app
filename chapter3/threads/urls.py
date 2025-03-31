from django.urls import path
from . import views

app_name = "threads"

urlpatterns = [
    path("", views.home, name="home"),
    path("thread/new/", views.thread_create, name="thread-create"),
    path("thread/<int:pk>/", views.thread_detail, name="thread-detail"),
    path("thread/<int:pk>/update/", views.thread_update, name="thread-update"),
    path("thread/<int:pk>/delete/", views.thread_delete, name="thread-delete"),
    path("thread/<int:pk>/like/", views.like_toggle, name="like-toggle"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment-delete"),
    path("follow/<str:username>/", views.follow_toggle, name="follow-toggle"),
    path("following/", views.following_feed, name="following-feed"),
    path("load-more/", views.load_more_threads, name="load-more"),
]
