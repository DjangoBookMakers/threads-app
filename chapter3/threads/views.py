from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Thread, Comment, Like, Follow
from .forms import ThreadForm, CommentForm


def home(request):
    threads = Thread.objects.all().order_by("-created_at")[:5]

    # 좋아요 상태 추가
    for thread in threads:
        thread.is_liked = False
        if request.user.is_authenticated:
            thread.is_liked = Like.objects.filter(
                user=request.user, thread=thread
            ).exists()

    return render(request, "threads/home.html", {"threads": threads})


def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    comments = thread.comments.all()

    # 댓글 작성 처리
    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.thread = thread
            comment.user = request.user
            comment.save()
            messages.success(request, "댓글이 작성되었습니다!")
            return redirect("threads:thread-detail", pk=thread.pk)
    else:
        comment_form = CommentForm()

    # 조회수 증가
    thread.views += 1
    thread.save(update_fields=["views"])

    # 좋아요 상태 추가
    thread.is_liked = False
    if request.user.is_authenticated:
        thread.is_liked = Like.objects.filter(user=request.user, thread=thread).exists()

    # 이전 및 다음 쓰레드 찾기
    prev_thread = (
        Thread.objects.filter(created_at__gt=thread.created_at)
        .order_by("created_at")
        .first()
    )
    next_thread = (
        Thread.objects.filter(created_at__lt=thread.created_at)
        .order_by("-created_at")
        .first()
    )

    context = {
        "thread": thread,
        "comments": comments,
        "comment_form": comment_form,
        "prev_thread": prev_thread,
        "next_thread": next_thread,
    }
    return render(request, "threads/thread_detail.html", context)


@login_required
def thread_create(request):
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.save()
            messages.success(request, "쓰레드가 작성되었습니다!")
            return redirect("threads:home")
    else:
        form = ThreadForm()

    return render(
        request, "threads/thread_form.html", {"form": form, "title": "새 쓰레드 작성"}
    )


@login_required
def thread_update(request, pk):
    thread = get_object_or_404(Thread, pk=pk)

    # 작성자만 수정할 수 있도록 확인
    if thread.user != request.user:
        messages.error(request, "다른 사용자의 쓰레드는 수정할 수 없습니다.")
        return redirect("threads:thread-detail", pk=thread.pk)

    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES, instance=thread)
        if form.is_valid():
            form.save()
            messages.success(request, "쓰레드가 수정되었습니다!")
            return redirect("threads:thread-detail", pk=thread.pk)
    else:
        form = ThreadForm(instance=thread)

    return render(
        request, "threads/thread_form.html", {"form": form, "title": "쓰레드 수정"}
    )


@login_required
def thread_delete(request, pk):
    thread = get_object_or_404(Thread, pk=pk)

    # 작성자만 삭제할 수 있도록 확인
    if thread.user != request.user:
        messages.error(request, "다른 사용자의 쓰레드는 삭제할 수 없습니다.")
        return redirect("threads:thread-detail", pk=thread.pk)

    if request.method == "POST":
        thread.delete()
        messages.success(request, "쓰레드가 삭제되었습니다!")
        return redirect("threads:home")

    return render(request, "threads/thread_confirm_delete.html", {"thread": thread})


def load_more_threads(request):
    threads = Thread.objects.all().order_by("-created_at")
    page_number = request.GET.get("page", 1)
    per_page = 5  # 한 번에 로드할 쓰레드 수

    paginator = Paginator(threads, per_page)

    # 요청된 페이지가 유효한지 확인
    if int(page_number) > paginator.num_pages:
        return JsonResponse(
            {
                "threads_html": "",
                "has_next": False,
                "next_page_number": None,
            }
        )

    page_obj = paginator.get_page(page_number)

    # 좋아요 상태 추가
    for thread in page_obj:
        thread.is_liked = False
        if request.user.is_authenticated:
            thread.is_liked = Like.objects.filter(
                user=request.user, thread=thread
            ).exists()

    # 쓰레드 HTML 렌더링
    threads_html = render_to_string(
        "threads/includes/thread_list.html", {"threads": page_obj}
    )

    # 응답 데이터 구성
    data = {
        "threads_html": threads_html,
        "has_next": page_obj.has_next(),
        "next_page_number": (
            page_obj.next_page_number() if page_obj.has_next() else None
        ),
    }

    return JsonResponse(data)


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    thread_id = comment.thread.id

    # 작성자만 삭제할 수 있도록 확인
    if comment.user != request.user:
        messages.error(request, "다른 사용자의 댓글은 삭제할 수 없습니다.")
        return redirect("threads:thread-detail", pk=thread_id)

    if request.method == "POST":
        comment.delete()
        messages.success(request, "댓글이 삭제되었습니다!")
        return redirect("threads:thread-detail", pk=thread_id)

    return render(request, "threads/comment_confirm_delete.html", {"comment": comment})


@login_required
def like_toggle(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    user = request.user

    # 이미 좋아요가 있는지 확인
    like_exists = Like.objects.filter(user=user, thread=thread).exists()

    if like_exists:
        # 좋아요가 이미 있으면 삭제 (좋아요 취소)
        Like.objects.filter(user=user, thread=thread).delete()
        liked = False
    else:
        # 좋아요가 없으면 생성 (좋아요 추가)
        Like.objects.create(user=user, thread=thread)
        liked = True

    # 비동기 요청인 경우 JSON 응답 반환
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"liked": liked, "total_likes": thread.likes.count()})

    # 일반 요청인 경우 이전 페이지로 리다이렉트
    return redirect(request.META.get("HTTP_REFERER", "threads:home"))


@login_required
def follow_toggle(request, username):
    # 자기 자신을 팔로우하는 것을 방지
    if request.user.username == username:
        messages.error(request, "자기 자신을 팔로우할 수 없습니다.")
        return redirect("users:profile", username=username)

    # 팔로우 대상 사용자 가져오기
    user_to_follow = get_object_or_404(User, username=username)

    # 이미 팔로우 중인지 확인
    follow_exists = Follow.objects.filter(
        follower=request.user, following=user_to_follow
    ).exists()

    if follow_exists:
        # 팔로우가 이미 있으면 삭제 (언팔로우)
        Follow.objects.filter(follower=request.user, following=user_to_follow).delete()
        messages.success(request, f"{username}님을 언팔로우하였습니다.")
    else:
        # 팔로우가 없으면 생성 (팔로우)
        Follow.objects.create(follower=request.user, following=user_to_follow)
        messages.success(request, f"{username}님을 팔로우하였습니다.")

    # 프로필 페이지로 리다이렉트
    return redirect("users:profile", username=username)


@login_required
def following_feed(request):
    # 사용자가 팔로우한 사용자 목록 가져오기
    following_users = User.objects.filter(followers__follower=request.user)

    # 팔로우한 사용자들과 자신의 쓰레드 가져오기
    threads = Thread.objects.filter(
        Q(user__in=following_users) | Q(user=request.user)
    ).order_by("-created_at")

    # 좋아요 상태 추가
    for thread in threads:
        thread.is_liked = False
        if request.user.is_authenticated:
            thread.is_liked = Like.objects.filter(
                user=request.user, thread=thread
            ).exists()

    return render(request, "threads/following_feed.html", {"threads": threads})
