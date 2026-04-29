"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from users.views import KakaoLogIn, NewTokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/v1/posts/", include("community.urls")),
    path("api/v1/records/", include("records.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/runningmates/", include("runningmates.urls")),
    path("api/v1/login/kakao/", KakaoLogIn.as_view()),
    path(
        "api/v1/login/token/refresh/",
        NewTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
