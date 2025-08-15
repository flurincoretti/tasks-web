from django.db import models
from django.utils import timezone

from utils.fields import ULIDField, generate_ulid


class BaseModel(models.Model):
    id = ULIDField(primary_key=True, editable=True)
    created_at = models.DateTimeField(editable=True)
    updated_at = models.DateTimeField(editable=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        update_timestamp = kwargs.pop("update_timestamp", True)
        if not self.id:
            self.id = generate_ulid()
        if not self.created_at:
            self.created_at = timezone.now()
        if self._state.adding:
            if not self.updated_at:
                self.updated_at = self.created_at
        elif update_timestamp and not kwargs.get("force_update"):
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
