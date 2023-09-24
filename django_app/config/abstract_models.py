import uuid

from django.db import models


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(verbose_name='creation date', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='modification date', auto_now=True)

    class Meta:
        abstract = True
