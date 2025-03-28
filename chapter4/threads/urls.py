from django.urls import path
from . import views

app_name = "threads"

urlpatterns = [
    path("", views.home, name="home"),
    path("explore/", views.explore, name="explore"),
    path("thread/new/", views.create_thread, name="create"),
    path("thread/<int:pk>/", views.thread_detail, name="detail"),
    path("thread/<int:pk>/edit/", views.update_thread, name="update"),
    path("thread/<int:pk>/delete/", views.delete_thread, name="delete"),
    path(
        "thread/<int:thread_id>/comment/", views.create_comment, name="create_comment"
    ),
    path("comment/<int:pk>/edit/", views.update_comment, name="update_comment"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
]
