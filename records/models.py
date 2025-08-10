from django.db import models
from common.models import CommonModel


# Create your models here.
class Record(CommonModel):

    owner = models.ForeignKey(
        "users.user",
        on_delete=models.CASCADE,
        related_name="records",
    )

    duration_sec = models.PositiveIntegerField()

    distance_m = models.PositiveIntegerField()

    pace = models.PositiveSmallIntegerField()

    kcal = models.PositiveIntegerField()

    route = models.TextField(
        blank=True,
        null=True,
    )
