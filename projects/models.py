from django.db import models

from utils.fields import ULIDField


class Project(models.Model):
    id = ULIDField(primary_key=True, editable=True)
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.title)
