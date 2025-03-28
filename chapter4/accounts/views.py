from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

    # 사용자의 스레드 목록 가져오기(Thread 모델이 구현되었다고 가정)
    # threads = Thread.objects.filter(author=user).order_by('-created_at')

    context = {
        "profile_user": user,  # 템플릿에서 현재 로그인한 user와 구분하기 위해 profile_user로 이름 지정
        # 'threads': threads,
        "is_owner": request.user == user,  # 프로필 소유자인지 확인
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
