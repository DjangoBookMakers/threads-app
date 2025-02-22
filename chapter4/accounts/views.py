from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def accounts_signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            return redirect("accounts_profile")  # 게시글 목록 페이지로 이동
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


def accounts_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # 로그인 처리
            return redirect("accounts_profile")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def accounts_logout(request):
    logout(request)
    return redirect("accounts_login")


@login_required
def accounts_profile(request):
    return render(request, "accounts/profile.html", {"user": request.user})
