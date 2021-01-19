import uuid

from django.contrib.auth import get_user_model
from django.db import models

from .querysets import ArchiveableQueryset

User = get_user_model()


class Archiveable(models.Model):
    class Meta:
        abstract = True

    archived = models.BooleanField(default=False)

    def archive(self):
        self.archived = True

    def unarchive(self):
        self.archived = False

    objects = ArchiveableQueryset.as_manager()


class HasUUID(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    @property
    def uuid_str(self):
        return str(self.uuid)

    @property
    def shortcode(self):
        return str(self.uuid).split('-')[0]
