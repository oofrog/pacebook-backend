from django.urls import path
from . import views

urlpatterns = [
    path("", views.RunGroups.as_view()),
    path("<int:pk>", views.RunGroupDetail.as_view()),
    path("<int:pk>/join", views.JoinRun.as_view()),
]
