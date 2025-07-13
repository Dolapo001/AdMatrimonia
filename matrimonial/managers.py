from django.db import models
from django.db.models import Q


class MatrimonyProfileQuerySet(models.QuerySet):
    def filter_by_user(self, user):
        return self.filter_by_user(user=user)

    def public_profiles(self):
        return self.select_related('user').prefetch_related('pictures')

    def apply_filters(self, params):
        qs = self
        q = params.get('q')
        gender = params.get('gender')
        religion = params.get('religion')
        education = params.get('education')

        if q:
            qs = qs.filter(
                Q(gender__icontains=q) |
                Q(education__icontains=q) |
                Q(religion__icontains=q)
            )
        if gender:
            qs = qs.filter(gender__iexact=gender)
        if religion:
            qs = qs.filter(religion__iexact=religion)
        if education:
            qs = qs.filter(education__iexact=education)

        return qs


class MatrimonyProfileManager(models.Manager):
    def get_queryset(self):
        return MatrimonyProfileQuerySet(self.model, using=self._db)

    def get_by_user_id(self, user_id):
        return self.get_queryset().filter(user__id=user_id).first()

    def list_profiles(self, filters=None):
        qs = self.get_queryset().public_profiles()
        if filters:
            qs = qs.apply_filters(filters)
        return qs
