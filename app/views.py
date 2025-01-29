from django.shortcuts import render, redirect
from .models import *
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    posts = Post.objects.all()
    all_posts_count = posts.count()
    quantity = int(request.GET.get("quantity", 3))
    posts = posts[:quantity]
    q = request.GET.get("q")

    if q:
        posts = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))

    return render(
        request, "home.html", {"posts": posts, "all_posts_count": all_posts_count}
    )


def post(request, pk):
    post_data = get_object_or_404(Post, pk=pk)

    if request.user.is_authenticated:
        post_data.views.add(request.user)

    post_comments = Comment.objects.filter(post=post_data)
    post_comments = Paginator(post_comments, 3)
    page = request.GET.get("page")
    post_comments = post_comments.get_page(page)

    form = CommentForm()

    if request.method == "POST":
        create_comment(request, post_data)
        return redirect("app:post", pk=post_data.pk)

    return render(
        request,
        "post.html",
        {"post": post_data, "form": form, "post_comments": post_comments},
    )


@login_required(login_url="users:login")
def create_post(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # html-код

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect("app:home")

    return render(request, "form.html", {"form": form})


@login_required(login_url="users:login")
def edit_post(request, pk):
    post_data = Post.objects.get(id=pk)

    if post_data.author != request.user:
        return render(request, "403.html")

    form = PostForm(request.POST or None, request.FILES or None, instance=post_data)

    if form.is_valid():
        form.save()
        return redirect("app:post", pk=pk)

    return render(request, "form.html", {"form": form})


@login_required(login_url="users:login")
def delete_post(request, pk):
    post_data = Post.objects.get(id=pk)

    if post_data.author != request.user:
        return render(request, "403.html")

    if request.method == "POST":
        post_data.delete()
        return redirect("app:home")

    return render(request, "delete_post.html", {"pk": pk})


def create_comment(request, post_data):
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post_data
        comment.save()


def comment_delete(request, pk):
    comment_data = Comment.objects.get(id=pk)

    if comment_data.author != request.user:
        return render(request, "403.html")

    if request.method == "POST":
        comment_data.delete()
        return redirect("app:post", pk=comment_data.post.pk)

    return render(request, "comment_delete.html", {"comment": comment_data})


@login_required(login_url="users:login")
def comment_edit(request, pk):
    comment_data = Comment.objects.get(id=pk)

    if comment_data.author != request.user:
        return render(request, "403.html")

    form = CommentForm(request.POST or None, instance=comment_data)

    if form.is_valid():
        instance = form.save(commit=False)

        if not instance.is_edited:
            instance.is_edited = True

        instance.save()

        return redirect("app:post", pk=comment_data.post.pk)

    return render(request, "form.html", {"form": form})


@login_required(login_url="users:login")
def post_like(request, pk):
    post_data = Post.objects.get(pk=pk)

    if request.user not in post_data.likes.all():
        post_data.likes.add(request.user)
        post_data.dislikes.remove(request.user)
    elif request.user in post_data.likes.all():
        post_data.likes.remove(request.user)

    return redirect("app:post", pk=pk)


@login_required(login_url="users:login")
def post_dislike(request, pk):
    post_data = Post.objects.get(pk=pk)

    if request.user not in post_data.dislikes.all():
        post_data.dislikes.add(request.user)
        post_data.likes.remove(request.user)
    elif request.user in post_data.dislikes.all():
        post_data.dislikes.remove(request.user)

    return redirect("app:post", pk=pk)


@login_required(login_url="users:login")
def comment_like(request, pk):
    comment = Comment.objects.get(pk=pk)
    user = request.user
    likes = comment.likes

    if user not in likes.all():
        likes.add(user)
        comment.dislikes.remove(user)
    elif user in likes.all():
        likes.remove(user)

    return redirect("app:post", pk=comment.post.pk)


@login_required(login_url="users:login")
def comment_dislike(request, pk):
    comment = Comment.objects.get(pk=pk)
    user = request.user
    dislikes = comment.dislikes

    if user not in dislikes.all():
        dislikes.add(user)
        comment.likes.remove(user)
    elif user in dislikes.all():
        dislikes.remove(user)

    return redirect("app:post", pk=comment.post.pk)


def reply(request, pk):
    form = CommentForm(request.POST or None)

    if form.is_valid():
        parent_comment = Comment.objects.get(pk=pk)
        instance = form.save(commit=False)

        instance.parent = parent_comment
        instance.author = request.user
        instance.post = parent_comment.post
        instance.save()
        return redirect("app:post", pk=parent_comment.post.pk)

    return render(request, "form.html", {"form": form})


def read_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    return render(request, "read_comment.html", {"comment": comment})
