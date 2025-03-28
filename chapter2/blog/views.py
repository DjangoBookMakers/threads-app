from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "blog/post_list.html", context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {"post": post}
    return render(request, "blog/post_detail.html", context)
