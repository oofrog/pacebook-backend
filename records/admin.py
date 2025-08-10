from django.contrib import admin
from .models import Record


# Register your models here.
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):

    list_display = (
        "owner",
        "duration_sec",
        "distance_m",
        "pace",
        "kcal",
        "route",
        "created_at",
        "updated_at",
    )
