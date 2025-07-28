from django.urls import path
from . import views

urlpatterns = [
    path("", views.Posts.as_view()),
    path("<int:pk>",views.PostDetail.as_view()),
    path("<int:pk>/comments",views.Comments.as_view()),
    path("<int:post_pk>/comments/<int:comment_pk>",views.CommentDetail.as_view()),
    path("<int:pk>/likes",views.Likes.as_view()),
]
