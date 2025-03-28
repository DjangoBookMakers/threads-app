from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, JsonResponse
from .models import Thread
from .forms import ThreadForm


def home(request):
    """
    홈 페이지 뷰 - 로그인한 사용자의 타임라인을 표시합니다.
    """
    threads = Thread.objects.all()

    if request.method == "POST" and request.user.is_authenticated:
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            messages.success(request, "스레드가 생성되었습니다!")
            return redirect("threads:home")
    else:
        form = ThreadForm()

    context = {
        "title": "홈",
        "threads": threads,
        "form": form,
    }
    return render(request, "threads/home.html", context)


def explore(request):
    """
    탐색 페이지 뷰 - 인기 스레드와 트렌드를 표시합니다.
    """
    # 임시로 모든 스레드 표시
    threads = Thread.objects.all()

    context = {
        "title": "탐색",
        "threads": threads,
    }
    return render(request, "threads/explore.html", context)


def thread_detail(request, pk):
    """
    스레드 상세 페이지 뷰
    """
    thread = get_object_or_404(Thread, pk=pk)

    context = {
        "thread": thread,
    }
    return render(request, "threads/thread_detail.html", context)


@login_required
def create_thread(request):
    """
    스레드 생성 뷰
    """
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            messages.success(request, "스레드가 생성되었습니다!")
            return redirect("threads:home")
    else:
        form = ThreadForm()

    context = {
        "form": form,
        "title": "새 스레드",
    }
    return render(request, "threads/create_thread.html", context)


@login_required
def update_thread(request, pk):
    """
    스레드 수정 뷰
    """
    thread = get_object_or_404(Thread, pk=pk)

    # 작성자만 수정 가능
    if thread.author != request.user:
        messages.error(request, "다른 사용자의 스레드는 수정할 수 없습니다.")
        return redirect("threads:detail", pk=pk)

    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES, instance=thread)
        if form.is_valid():
            form.save()
            messages.success(request, "스레드가 수정되었습니다!")
            return redirect("threads:detail", pk=pk)
    else:
        form = ThreadForm(instance=thread)

    context = {
        "form": form,
        "thread": thread,
        "title": "스레드 수정",
    }
    return render(request, "threads/update_thread.html", context)


@login_required
def delete_thread(request, pk):
    """
    스레드 삭제 뷰
    """
    thread = get_object_or_404(Thread, pk=pk)

    # 작성자만 삭제 가능
    if thread.author != request.user:
        messages.error(request, "다른 사용자의 스레드는 삭제할 수 없습니다.")
        return redirect("threads:detail", pk=pk)

    if request.method == "POST":
        thread.delete()
        messages.success(request, "스레드가 삭제되었습니다!")
        return redirect("threads:home")

    context = {
        "thread": thread,
        "title": "스레드 삭제",
    }
    return render(request, "threads/delete_thread.html", context)
