import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User
from .serializers import KakaoLogInSerializer, PrivateUserSerializer


@extend_schema(tags=["Login"])
class KakaoLogIn(APIView):

    @extend_schema(request=KakaoLogInSerializer)
    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response(
                {"error": "code is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_CLIENT_ID,
                    "redirect_uri": settings.KAKAO_REDIRECT_URI,
                    "code": code,
                },
            )
            if not access_token:
                return Response(
                    {"error": "token ???"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            email = kakao_account.get("email")
            username, _ = email.split("@")
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "email": email,
                    "username": username,
                    "name": profile.get("nickname"),
                },
            )

            if created:
                user.set_unusable_password()
                user.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Login"])
class NewTokenRefreshView(TokenRefreshView):
    """JWT 토큰 재발급"""

    pass


@extend_schema(tags=["Users"])
class UserMe(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(request=PrivateUserSerializer)
    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
