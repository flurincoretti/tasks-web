import ulid
from django.db import models


def generate_ulid() -> str:
    return ulid.new().str


class ULIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 26)
        kwargs.setdefault("default", generate_ulid)
        kwargs.setdefault("editable", False)
        super().__init__(*args, **kwargs)
