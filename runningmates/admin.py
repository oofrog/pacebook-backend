from django.contrib import admin
from .models import RunGroup, RunParticipant


@admin.register(RunGroup)
class RunGroupAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "scheduled_time",
        "location_lat",
        "location_lng",
        "pace",
        "distance_km",
        "description",
    )


@admin.register(RunParticipant)
class RunParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "group",
    )
