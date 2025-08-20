from rest_framework import serializers
from .models import RunGroup, RunParticipant
from users.serializers import TinyUserSerializer


class RunGroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = RunGroup
        fields = (
            "host",
            "place",
        )


class RunGroupDetailSerializer(serializers.ModelSerializer):

    host = TinyUserSerializer(read_only=True)

    class Meta:
        model = RunGroup
        fields = "__all__"


class JoinOrLeaveRunSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)
    group = RunGroupListSerializer(read_only=True)

    class Meta:
        model = RunParticipant
        fields = "__all__"
