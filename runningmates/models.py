from django.db import models
from common.models import CommonModel


class RunGroup(CommonModel):
    title = models.CharField(max_length=50)
    scheduled_time = models.DateTimeField()
    location_lat = models.DecimalField(max_digits=9, decimal_places=6) #위도
    location_lng = models.DecimalField(max_digits=9, decimal_places=6) #경도
    pace = models.PositiveIntegerField()
    distance_km = models.PositiveIntegerField()
    description = models.TextField(blank=True)


class RunParticipant(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "runningmates.RunGroup",
        on_delete=models.CASCADE,
    )
