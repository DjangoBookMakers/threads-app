from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "post/list.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "post/detail.html", {"post": post})


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
