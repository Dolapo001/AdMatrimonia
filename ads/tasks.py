from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Ad
import logging

logger = logging.getLogger(__name__)


@shared_task
def activate_pending_ads():
    threshold = timezone.now() - timedelta(minutes=15)

    all_pending = Ad.objects.filter(status='pending')
    eligible_ads = all_pending.filter(pending_since__lte=threshold)

    activated_count = 0

    for ad in eligible_ads:
        logger.info(f"Activating ad: {ad.title}, pending_since={ad.pending_since}")
        ad.status = 'active'
        ad.save()
        activated_count += 1

    # Log skipped ads
    for ad in all_pending.exclude(id__in=eligible_ads):
        if ad.pending_since is None:
            logger.warning(f"Skipped ad (no pending_since): {ad.title}")
        else:
            logger.info(f"Skipped ad (too recent): {ad.title} - pending_since={ad.pending_since}")

    logger.info(f"{activated_count} pending ads activated.")
    return f"{activated_count} ads activated."
