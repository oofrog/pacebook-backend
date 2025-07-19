from rest_framework.serializers import ModelSerializer
from .models import Post
from users.serializers import TinyUserSerializer

class PostListSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = (
            "pk",
            "owner",
            "payload",
            "created_at",
        )

class PostDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
