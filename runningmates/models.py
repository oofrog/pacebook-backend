from django.db import models
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.models import CommonModel

class RunningMate(CommonModel):
    leader = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="runningmates_led",
    )  # 작성자
    place = models.CharField(max_length=100)               # 장소 
    scheduled_time = models.TimeField()                # 달릴 시간
    pace = models.PositiveIntegerField(null=True,blank=True)
    description = models.TextField(blank=True)             # 상세 설명
    max_participants = models.PositiveIntegerField(default=4)  # 최대 모집 인원


    def __str__(self):
        return f"{self.place} - {self.scheduled_time.strftime('%Y-%m-%d %H:%M')} by {self.leader.username}"

class RunParticipant(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "runningmates.RunningMate",
        on_delete=models.CASCADE,
    )