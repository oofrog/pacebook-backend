from django.contrib import admin
from .models import Post, Photo, Like, Comment

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "owner",
        "payload",
        "created_at",
    )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):

    list_display = (
        "file",
        "post",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "post",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "post",
        "payload",
        "created_at",
    )
