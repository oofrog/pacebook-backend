import re
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import RecordDetailSerializer
from .models import Record


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


class MyRecords(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = str(timezone.localdate())
        date_str = request.query_params.get("date", today)
        pattern = r"^(?!0000-00-00)\d{4}-\d{2}-\d{2}$"
        if not re.match(pattern, date_str):
            date_str = today
        target_records = Record.objects.filter(created_at__startswith=date_str)
        serializer = RecordDetailSerializer(
            target_records,
            many=True,
        )
        return Response(serializer.data)
