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


class PartnerPreferenceQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user).first()


class PartnerPreferenceManager(models.Manager):
    def get_queryset(self):
        return PartnerPreferenceQuerySet(self.model, using=self._db)

    def get_for_user(self, user):
        return self.get_queryset().for_user(user)


class ConnectionRequestManager(models.Manager):
    def send(self, sender, receiver, message=None):
        if sender == receiver:
            raise ValueError("You cannot send a request to yourself")

        obj, created = self.get_or_create(
            sender=sender,
            receiver=receiver,
            defaults={'message': message}
        )
        return obj, created

    def get_received(self, user):
        return self.filter(receiver=user, status='pending')

    def get_sent(self, user):
        return self.filter(sender=user)

    def respond(self, sender, receiver, status_value):
        request = self.filter(sender=sender, receiver=receiver).first()
        if request:
            request.status = status_value
            request.save()
            return request
        return None


class BookmarkManager(models.Manager):
    def toggle(self, user, profile):
        bookmark, created = self.get_or_create(user=user, profile=profile)
        if not created:
            bookmark.delete()
            return False  # Unbookmarked
        return True  # Bookmarked

    def get_user_bookmarks(self, user):
        return self.filter(user=user)
