from django.urls import path
from . import views

urlpatterns = [
    path("kakao", views.KakaoLogIn.as_view()),
]
