from rest_framework.urls import path
from . import views

urlpatterns = [
    path("", views.Posts.as_view()),
]
