from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, logout


def log_in(request):
    form = LoginForm(data=request.POST or None)

    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("app:home")

    return render(request, "login.html", {"form": form})
