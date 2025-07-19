from django.db import models
import uuid6


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid6.uuid7,
        editable=False,
        unique=True
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ("-id", "id")

