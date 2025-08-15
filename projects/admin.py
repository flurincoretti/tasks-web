from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = (
        "title",
        "id",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "title",
                )
            },
        ),
    )
