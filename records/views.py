from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import RecordDetailSerializer


class Records(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=RecordDetailSerializer)
    def post(self, request):
        serializer = RecordDetailSerializer(data=request.data)
        if serializer.is_valid():
            new_record = serializer.save(
                owner=request.user,
            )
            serializer = RecordDetailSerializer(new_record)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )