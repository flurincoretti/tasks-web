from django.contrib import admin

from .models import Timeblock


@admin.register(Timeblock)
class TimeblockAdmin(admin.ModelAdmin):
    list_filter = ["project"]
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = (
        "started_at",
        "ended_at",
        "id",
    )
    list_display_links = ("id",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "project",
                    "notes",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "started_at",
                    "ended_at",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
