from rest_framework import serializers
from .models import Record
from users.serializers import TinyUserSerializer


class RecordDetailSerializer(serializers.ModelSerializer):

    owner = TinyUserSerializer(read_only=True)

    class Meta:
        model = Record
        fields = "__all__"
