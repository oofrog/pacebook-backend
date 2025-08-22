from django.db import models
from common.models import CommonModel


class RunGroup(CommonModel):
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="runningmates_led",
    )
    place = models.CharField(max_length=100)
    scheduled_time = models.TimeField()
    target_pace = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    max_participants = models.PositiveIntegerField(default=4)


class RunParticipant(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "runningmates.RunGroup",
        on_delete=models.CASCADE,
    )
