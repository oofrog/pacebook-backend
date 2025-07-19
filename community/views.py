from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostListSerializer


class Posts(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostListSerializer(
            posts,
            many=True,
        )
        return Response(serializer.data)
