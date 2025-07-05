from random import random
from ads.constants import CATEGORY_CODE_MAP
from ads.models import Ad


def generate_unique_public_id(category_slug):
    code = CATEGORY_CODE_MAP.get(category_slug, 'GEN')
    for _ in range(100):  # to avoid infinite loop
        random_number = random.randint(1000, 9999)
        public_id = f"{code}{random_number}"
        if not Ad.objects.filter(public_id=public_id).exists():
            return public_id
    raise Exception("Unable to generate unique public_id")
