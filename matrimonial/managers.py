from django.db import models
from django.db.models import Q


class MatrimonyProfileQuerySet(models.QuerySet):
    def filter_by_user(self, user):
        return self.filter_by_user(user=user)

    def public_profiles(self):
        return self.select_related('user').prefetch_related('pictures')


class MatrimonyProfileManager(models.Manager):
    def get_queryset(self):
        return MatrimonyProfileQuerySet(self.model, using=self._db)

    def get_by_user_id(self, user_id):
        return self.get_queryset().filter(user__id=user_id).first()

    def list_profiles(self, filters=None):
        qs = self.get_queryset().public_profiles()
        if filters:
            qs = qs.filter(**filters)
        return qs
