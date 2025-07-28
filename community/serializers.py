from rest_framework.serializers import ModelSerializer
from .models import Post, Comment, Like
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


class CommentSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    post = PostListSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class LikeSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    post = PostListSerializer(read_only=True)

    class Meta:
        model = Like
        exclude = (
            "created_at",
            "updated_at",
        )
