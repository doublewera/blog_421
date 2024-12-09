from django.shortcuts import render
from .models import *
from django.http import HttpResponse


def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

def post(request, pk):
    return render(request, 'post.html', {})
