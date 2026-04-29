from django.urls import path
from . import views

urlpatterns = [
    path("me", views.UserMe.as_view()),
]
