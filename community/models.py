from django.db import models
from common.models import CommonModel


# Create your models here.
class Post(CommonModel):

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="posts",
    )
    payload = models.TextField()


class Photo(CommonModel):

    file = models.URLField()
    post = models.ForeignKey(
        "community.Post",
        on_delete=models.CASCADE,
        related_name="photos",
    )


class Like(CommonModel):

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    post = models.ForeignKey(
        "community.Post",
        on_delete=models.CASCADE,
        related_name="likes",
    )


class Comment(CommonModel):

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    post = models.ForeignKey(
        "community.Post",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    payload = models.CharField(
        max_length=50,
    )
