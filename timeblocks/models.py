from django.db import models
from django.utils import timezone

from projects.models import Project
from utils.models import BaseModel


class Timeblock(BaseModel):
    log = models.TextField(blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="timeblocks",
    )
    started_at = models.DateTimeField(default=timezone.now, blank=False)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_open(self) -> bool:
        return self.ended_at is None or self.ended_at == ""
