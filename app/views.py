from django.shortcuts import render, redirect
from .models import *
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})


def post(request, pk):
    # post_data = Post.objects.get_ob(id=pk) # было
    post_data = get_object_or_404(Post, pk=pk) # стало
    return render(request, "post.html", {"post": post_data})


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

    return render(request, "post_form.html", {"form": form})


@login_required(login_url="users:login")
def edit_post(request, pk):
    post_data = Post.objects.get(id=pk)

    if post_data.author != request.user:
        return render(request, '403.html')


    form = PostForm(request.POST or None, request.FILES or None, instance=post_data)

    if form.is_valid():
        form.save()
        return redirect("app:post", pk=pk)

    return render(request, "post_form.html", {"form": form})


@login_required(login_url="users:login")
def delete_post(request, pk):
    post_data = Post.objects.get(id=pk)

    if post_data.author != request.user:
        return render(request, '403.html')

    if request.method == "POST":
        post_data.delete()
        return redirect("app:home")

    return render(request, "delete_post.html", {"pk": pk})
