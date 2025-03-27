from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            messages.success(request, "회원가입이 완료되었습니다!")
            return redirect("home")
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
                next_url = request.POST.get("next", "home")
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
    return redirect("home")
