from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("post/<int:pk>/", post, name="post"),
    path("create_post/", create_post, name="create_post"),
    path("edit_post/<int:pk>", edit_post, name="edit_post"),
    path('delete_post/<int:pk>', delete_post, name='delete_post'),
    path('comment_delete/<int:pk>', comment_delete, name='comment_delete'),
    path('comment_edit/<int:pk>', comment_edit, name='comment_edit'),
    path('post_like/<int:pk>', post_like, name='post_like'),
    path('post_dislike/<int:pk>', post_dislike, name='post_dislike'),
    path('comment_like/<int:pk>', comment_like, name='comment_like'),
    path('comment_dislike/<int:pk>', comment_dislike, name='comment_dislike'),
    path('reply/<int:pk>/', reply, name='reply'),
    path('read_comment/<int:pk>', read_comment, name='read_comment'),
] 