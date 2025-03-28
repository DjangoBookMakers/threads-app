from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, JsonResponse
from .models import Thread, Comment
from .forms import ThreadForm, CommentForm


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


def thread_detail(request, pk):
    """
    스레드 상세 페이지 뷰
    """
    thread = get_object_or_404(Thread, pk=pk)
    comments = thread.comments.all()

    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()
            messages.success(request, "댓글이 작성되었습니다.")
            return redirect("threads:detail", pk=pk)
    else:
        form = CommentForm()

    context = {
        "thread": thread,
        "comments": comments,
        "form": form,
    }
    return render(request, "threads/thread_detail.html", context)


@login_required
def create_comment(request, thread_id):
    """
    댓글 생성 뷰
    """
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()
            messages.success(request, "댓글이 작성되었습니다.")

            # AJAX 요청인 경우 JSON 응답
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "status": "success",
                        "author": request.user.username,
                        "content": comment.content,
                        "created_at": comment.created_at.strftime(
                            "%Y년 %m월 %d일 %H:%M"
                        ),
                    }
                )

    return redirect("threads:detail", pk=thread_id)


@login_required
def update_comment(request, pk):
    """
    댓글 수정 뷰
    """
    comment = get_object_or_404(Comment, pk=pk)

    # 작성자만 수정 가능
    if comment.author != request.user:
        messages.error(request, "다른 사용자의 댓글은 수정할 수 없습니다.")
        return redirect("threads:detail", pk=comment.thread.pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "댓글이 수정되었습니다.")
            return redirect("threads:detail", pk=comment.thread.pk)
    else:
        form = CommentForm(instance=comment)

    context = {
        "form": form,
        "comment": comment,
        "thread": comment.thread,
    }
    return render(request, "threads/update_comment.html", context)


@login_required
def delete_comment(request, pk):
    """
    댓글 삭제 뷰
    """
    comment = get_object_or_404(Comment, pk=pk)

    # 작성자만 삭제 가능
    if comment.author != request.user:
        messages.error(request, "다른 사용자의 댓글은 삭제할 수 없습니다.")
        return redirect("threads:detail", pk=comment.thread.pk)

    thread_id = comment.thread.id

    if request.method == "POST":
        comment.delete()
        messages.success(request, "댓글이 삭제되었습니다.")

        # AJAX 요청인 경우 JSON 응답
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"status": "success"})

    return redirect("threads:detail", pk=thread_id)


@login_required
def like_thread(request, pk):
    """
    스레드 좋아요 토글 API
    """
    thread = get_object_or_404(Thread, pk=pk)

    # 이미 좋아요를 눌렀는지 확인
    if thread.likes.filter(id=request.user.id).exists():
        # 좋아요 취소
        thread.likes.remove(request.user)
        liked = False
    else:
        # 좋아요 추가
        thread.likes.add(request.user)
        liked = True

    return JsonResponse(
        {"status": "success", "liked": liked, "like_count": thread.get_like_count()}
    )


@login_required
def like_comment(request, pk):
    """
    댓글 좋아요 토글 API
    """
    comment = get_object_or_404(Comment, pk=pk)

    # 이미 좋아요를 눌렀는지 확인
    if comment.likes.filter(id=request.user.id).exists():
        # 좋아요 취소
        comment.likes.remove(request.user)
        liked = False
    else:
        # 좋아요 추가
        comment.likes.add(request.user)
        liked = True

    return JsonResponse(
        {"status": "success", "liked": liked, "like_count": comment.get_like_count()}
    )
