from django.contrib import admin
from .models import RunningMate,RunParticipant


@admin.register(RunningMate)
class RunningMateAdmin(admin.ModelAdmin):
    list_display=(
        "leader",
        "place",
        "scheduled_time",
    )

@admin.register(RunParticipant)
class RunParticipantAdmin(admin.ModelAdmin):
    list_display=(
        "user",
        "group",
    )