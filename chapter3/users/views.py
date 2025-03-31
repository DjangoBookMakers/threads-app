from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from threads.models import Like, Follow


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request,
                f"{username}님의 계정이 생성되었습니다! 이제 로그인할 수 있습니다.",
            )
            return redirect("users:login")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    threads = user.thread_set.all()

    # 좋아요 상태 추가
    for thread in threads:
        thread.is_liked = False
        if request.user.is_authenticated:
            thread.is_liked = Like.objects.filter(
                user=request.user, thread=thread
            ).exists()

    # 팔로우 상태 확인
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()

    # 팔로워 및 팔로잉 수
    followers_count = user.followers.count()
    following_count = user.following.count()

    context = {
        "profile_user": user,
        "threads": threads,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count,
    }
    return render(request, "users/profile.html", context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "프로필이 업데이트되었습니다!")
            return redirect("users:profile", username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/edit_profile.html", context)
