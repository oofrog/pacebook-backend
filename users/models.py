from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    avatar = models.URLField(
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=150,
        default="",
    )
    gender = models.CharField(
        max_length=150,
        choices=GenderChoices,
        default=GenderChoices.MALE,
    )
    birth_day = models.DateField(
        null=True,
        blank=True,
    )
