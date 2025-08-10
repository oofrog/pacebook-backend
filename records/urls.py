from django.urls import path
from . import views

urlpatterns = [
    path("", views.Records.as_view()),
    path("me", views.MyRecords.as_view()),
]
