from rest_framework import serializers
from .models import User


class TinyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
        )


class KakaoLogInSerializer(serializers.Serializer):
    code = serializers.CharField()
