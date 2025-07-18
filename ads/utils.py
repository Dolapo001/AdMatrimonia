import random
from ads.constants import CATEGORY_CODE_MAP


def generate_unique_publik_id(category_slug):
    from .models import Ad  # Local import to avoid circular dependency

    code = CATEGORY_CODE_MAP.get(category_slug, 'GEN')
    for _ in range(100):
        random_number = random.randint(1000, 9999)
        publik_id = f"{code}{random_number}"
        if not Ad.objects.filter(publik_id=publik_id).exists():
            return publik_id
    raise Exception("Unable to generate unique publik_id")