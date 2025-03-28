from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import SignUpForm, LoginForm, ProfileEditForm
from .models import User


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            messages.success(request, "회원가입이 완료되었습니다!")
            return redirect("threads:home")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # 로그인 상태 유지 옵션 처리
                if not remember_me:
                    # 브라우저를 닫으면 세션 만료
                    request.session.set_expiry(0)

                messages.success(request, f"{username}님, 환영합니다!")
                next_url = request.POST.get("next", "threads:home")
                return redirect(next_url)
            else:
                messages.error(
                    request,
                    "로그인에 실패했습니다. 사용자 이름과 비밀번호를 확인해주세요.",
                )
        else:
            messages.error(request, "로그인에 실패했습니다. 입력 내용을 확인해주세요.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "로그아웃 되었습니다.")
    return redirect("threads:home")


def profile_view(request, username):
    """
    사용자 프로필 페이지를 표시합니다.
    """
    user = get_object_or_404(User, username=username)

    # 처음에는 10개만 로드
    limit = 10
    threads = (
        user.threads.select_related("author").all().order_by("-created_at")[:limit]
    )

    # 더 많은 스레드가 있는지 확인
    has_more = user.threads.count() > limit

    context = {
        "profile_user": user,
        "threads": threads,
        "is_owner": request.user == user,
        "threads_count": user.threads.count(),
        "comments_count": user.comments.count(),
        "has_more": has_more,
    }

    return render(request, "accounts/profile.html", context)


@login_required
def edit_profile(request):
    """
    사용자 프로필 편집 페이지입니다.
    """
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 업데이트되었습니다.")
            return redirect("accounts:profile", username=request.user.username)
        else:
            messages.error(
                request, "프로필 업데이트에 실패했습니다. 입력 내용을 확인해주세요."
            )
    else:
        form = ProfileEditForm(instance=request.user)

    context = {
        "form": form,
    }

    return render(request, "accounts/edit_profile.html", context)


def user_threads_api(request, username):
    """
    사용자 스레드를 JSON 형식으로 반환하는 API
    """
    user = get_object_or_404(User, username=username)
    offset = int(request.GET.get("offset", 0))
    limit = 10  # 한 번에 로드할 스레드 수

    threads = (
        user.threads.select_related("author")
        .all()
        .order_by("-created_at")[offset : offset + limit + 1]
    )
    has_more = len(threads) > limit

    if has_more:
        threads = threads[:limit]

    # 스레드 HTML 렌더링
    threads_html = ""
    for thread in threads:
        threads_html += render_to_string(
            "threads/partials/thread_card.html",
            {
                "thread": thread,
                "user": request.user,
            },
            request=request,
        )

    return JsonResponse(
        {
            "html": threads_html,
            "has_more": has_more,
        }
    )


@login_required
def follow_toggle(request, username):
    """
    사용자 팔로우 토글 API
    """
    user_to_follow = get_object_or_404(User, username=username)

    # 자기 자신은 팔로우할 수 없음
    if request.user == user_to_follow:
        return JsonResponse(
            {"status": "error", "message": "자기 자신을 팔로우할 수 없습니다."}
        )

    # 이미 팔로우하고 있는지 확인
    if request.user.following.filter(username=username).exists():
        # 팔로우 취소
        request.user.following.remove(user_to_follow)
        is_following = False
    else:
        # 팔로우 추가
        request.user.following.add(user_to_follow)
        is_following = True

    return JsonResponse(
        {
            "status": "success",
            "is_following": is_following,
            "followers_count": user_to_follow.get_followers_count(),
            "following_count": user_to_follow.get_following_count(),
        }
    )


def followers_list(request, username):
    """
    팔로워 목록 보기
    """
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()

    context = {
        "profile_user": user,
        "followers": followers,
        "is_owner": request.user == user,
    }

    return render(request, "accounts/followers_list.html", context)


def following_list(request, username):
    """
    팔로잉 목록 보기
    """
    user = get_object_or_404(User, username=username)
    following = user.following.all()

    context = {
        "profile_user": user,
        "following": following,
        "is_owner": request.user == user,
    }

    return render(request, "accounts/following_list.html", context)
