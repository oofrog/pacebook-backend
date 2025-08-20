from django.contrib import admin
from .models import RunGroup, RunParticipant


@admin.register(RunGroup)
class RunGroupAdmin(admin.ModelAdmin):
    list_display = (
        "host",
        "place",
        "scheduled_time",
    )


@admin.register(RunParticipant)
class RunParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "group",
    )
