from django.db import models
from django.utils import timezone


class AdQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status='active', is_expired=False)

    def for_user(self, user):
        return self.filter(user=user)

    def order_recent(self):
        return self.order_by('-created_at')


class AdManager(models.Manager):
    def get_queryset(self):
        return AdQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def order_recent(self):
        return self.get_queryset().order_recent()


class FavoriteAdQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


class FavoriteAdManager(models.Manager):
    def get_queryset(self):
        return FavoriteAdQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)


class CategoryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True).order_by('order')


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class SubCategoryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True).order_by('order')


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return SubCategoryQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()