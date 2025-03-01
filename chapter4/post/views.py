from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "post/list.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by("-created_at")

    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(
        request,
        "post/detail.html",
        {"post": post, "comments": comments, "comment_form": comment_form},
    )


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm()
    return render(request, "post/create.html", {"form": form})


@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 작성자 체크
    if post.author != request.user:
        return redirect("post_detail", post_id=post.id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "post/update.html", {"form": form, "post_id": post_id})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 작성자 체크
    if post.author != request.user:
        return redirect("post_detail", post_id=post.id)

    if request.method == "POST":
        post.delete()
        return redirect("post_list")

    return redirect("post_detail", post_id=post.id)


@login_required
def comment_update(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)

    # 댓글 작성자 확인
    if comment.author != request.user:
        return redirect("post_detail", post_id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("post_detail", post_id=post_id)
    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        "post/comment_update.html",
        {"form": form, "post": post, "comment": comment},
    )


@login_required
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # 댓글 작성자 확인
    if comment.author != request.user:
        return redirect("post_detail", post_id=post_id)

    if request.method == "POST":
        comment.delete()

    return redirect("post_detail", post_id=post_id)
