from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import *


def log_in(request):
    form = LoginForm(data=request.POST or None)

    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("app:home")

    return render(request, "auth.html", {"form": form, "title": "Вход"})


def log_out(request):
    logout(request)
    return redirect("app:home")


def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("users:login")

    return render(request, "auth.html", {"form": form, "title": "Регистрация"})
