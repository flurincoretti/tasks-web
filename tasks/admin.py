from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ["description"]
    list_filter = ("project", "status", "priority")
    readonly_fields = ("id", "created_at", "updated_at", "completed_at")
    list_display = (
        "id",
        "description",
        "project",
        "status",
        "priority",
        "due_at",
        "completed_at",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "description",
                    "notes",
                    "project",
                    "status",
                    "priority",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "due_at",
                    "completed_at",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
