from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer


class Posts(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostListSerializer(
            posts,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostDetailSerializer(data=request.data)
        if serializer.is_valid():
            new_post = serializer.save(
                owner=request.user,
            )
            serializer = PostDetailSerializer(new_post)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PostDetail(APIView):

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
