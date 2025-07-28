from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from .models import Post, Comment, Like
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
    LikeSerializer,
)


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
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class PostDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        if post.owner != request.user:
            raise PermissionDenied
        serializer = PostDetailSerializer(
            post,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_post = serializer.save()
            serializer = PostDetailSerializer(updated_post)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.owner != request.user:
            raise PermissionDenied
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Comments(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        post = self.get_post(pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(
            comments,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        post = self.get_post(pk)
        serialiizer = CommentSerializer(data=request.data)
        if serialiizer.is_valid():
            new_comment = serialiizer.save(
                post=post,
                user=request.user,
            )
            serialiizer = CommentSerializer(new_comment)
            return Response(serialiizer.data)
        else:
            return Response(
                serialiizer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class CommentDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_comment(self, comment_pk):
        try:
            return Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound

    def patch(self, request, post_pk, comment_pk):
        comment = self.get_comment(comment_pk)
        if comment.user != request.user:
            raise PermissionDenied
        serializer = CommentSerializer(
            comment,
            data=request.data,
        )
        if serializer.is_valid():
            updated_comment = serializer.save()
            serializer = CommentSerializer(updated_comment)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, post_pk, comment_pk):
        comment = self.get_comment(comment_pk)
        if comment.user != request.user:
            raise PermissionDenied
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Likes(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        post = self.get_post(pk)
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(
            likes,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        post = self.get_post(pk)
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            new_like = serializer.save(
                user=request.user,
                post=post,
            )
            serializer = LikeSerializer(new_like)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        post = self.get_post(pk)
        try:
            like = Like.objects.get(
                user=request.user,
                post=post,
            )
        except  Like.DoesNotExist:
            raise NotFound
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
