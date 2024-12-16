from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("post/<int:pk>/", post, name="post"),
    path("create_post/", create_post, name="create_post"),
    path("edit_post/<int:pk>", edit_post, name="edit_post"),
]