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


class PrivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "email",
            "name",
            "gender",
            "birth_day",
        )
        read_only_fields = (
            "username",
            "email",
        )
