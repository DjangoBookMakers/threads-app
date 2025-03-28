from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path(
        "profile/<str:username>/threads/",
        views.user_threads_api,
        name="user_threads_api",
    ),
    path("follow/<str:username>/", views.follow_toggle, name="follow_toggle"),
    path(
        "profile/<str:username>/followers/", views.followers_list, name="followers_list"
    ),
    path(
        "profile/<str:username>/following/", views.following_list, name="following_list"
    ),
]
