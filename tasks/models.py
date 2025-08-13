from django.db import models
from django.db.models import TextChoices
from django.utils import timezone

from projects.models import Project
from utils.models import BaseModel


class Task(BaseModel):
    class Priority(TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class Status(TextChoices):
        OPEN = "open", "Open"
        ONGOING = "ongoing", "Ongoing"
        DONE = "done", "Done"
        OBSOLETE = "obsolete", "Obsolete"

    description = models.CharField(max_length=255, blank=False)
    notes = models.TextField(blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN,
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    due_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.description)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        prev_status = None
        if self.pk:
            prev_status = (
                type(self)
                .objects.filter(pk=self.pk)
                .values_list("status", flat=True)
                .first()
            )

        if self.status == self.Status.DONE:
            # New or updated-to-DONE → ensure a timestamp exists
            if not self.completed_at:
                self.completed_at = timezone.now()
        elif prev_status == self.Status.DONE:
            # Moved away from DONE → clear timestamp
            self.completed_at = None

        super().save(*args, **kwargs)

    def mark_as_done(self) -> None:
        self.status = self.Status.DONE
        self.save()

    @property
    def is_overdue(self) -> bool:
        return (
            self.due_at
            and self.due_at < timezone.now()
            and self.status != self.Status.DONE
        )
