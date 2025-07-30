from django.db import models
from common.models import CommonModel

# Create your models here.


class Record(CommonModel):

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="records",
    )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    distance = models.FloatField()
    route = models.JSONField(
        null=True,
        blank=True,
    )

    def duration(self):
        return (self.ended_at - self.started_at).total_seconds()
