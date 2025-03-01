from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("new/", views.post_create, name="post_create"),
    path("<int:post_id>/", views.post_detail, name="post_detail"),
    path("<int:post_id>/edit/", views.post_update, name="post_update"),
    path("<int:post_id>/delete/", views.post_delete, name="post_delete"),
    path(
        "<int:post_id>/comments/<int:comment_id>/edit/",
        views.comment_update,
        name="comment_update",
    ),
    path(
        "<int:post_id>/comments/<int:comment_id>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
]
