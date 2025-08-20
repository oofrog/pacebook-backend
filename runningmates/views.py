from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import RunGroup, RunParticipant
from .serializers import (
    RunGroupListSerializer,
    RunGroupDetailSerializer,
    JoinOrLeaveRunSerializer,
)


@extend_schema(tags=["RunningMates"])
class RunGroups(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):

        groups = RunGroup.objects.all()
        serializer = RunGroupListSerializer(
            groups,
            many=True,
        )
        return Response(serializer.data)

    @extend_schema(request=RunGroupDetailSerializer)
    def post(self, request):

        serializer = RunGroupDetailSerializer(data=request.data)
        if serializer.is_valid():
            new_group = serializer.save(
                host=request.user,
            )
            serializer = RunGroupDetailSerializer(new_group)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(tags=["RunningMates"])
class RunGroupDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return RunGroup.objects.get(pk=pk)
        except RunGroup.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = RunGroupDetailSerializer(group)
        return Response(serializer.data)

    @extend_schema(request=RunGroupDetailSerializer)
    def patch(self, request, pk):
        group = self.get_object(pk)
        serializer = RunGroupDetailSerializer(
            group,
            data=request.data,
        )
        if serializer.is_valid():
            updated_group = serializer.save()
            serializer = RunGroupDetailSerializer(updated_group)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group = self.get_object(pk)
        if group.host != request.user:
            raise PermissionDenied
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JoinRun(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return RunGroup.objects.get(pk=pk)
        except RunGroup.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        group = self.get_object(pk)
        serializer = JoinOrLeaveRunSerializer(data=request.data)
        if serializer.is_valid():
            join_group = serializer.save(
                user=request.user,
                group=group,
            )
            serializer = JoinOrLeaveRunSerializer(join_group)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group = self.get_object(pk)
        try:
            participant = RunParticipant.objects.get(
                user=request.user,
                group=group,
            )
        except RunParticipant.DoesNotExist:
            raise NotFound
        participant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
