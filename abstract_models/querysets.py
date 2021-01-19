from django.db import models
from django.db.models import Q


class ArchiveableQueryset(models.QuerySet):
    _Q_ARCHIVED = Q(archived=True)

    def active(self):
        return self.filter(~ArchiveableQueryset._Q_ARCHIVED)

    def archived(self):
        return self.filter(ArchiveableQueryset._Q_ARCHIVED)
