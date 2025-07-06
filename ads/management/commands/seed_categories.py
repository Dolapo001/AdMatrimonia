from django.core.management.base import BaseCommand
from ads.models import Category, SubCategory
from ads.constants import *
from django.utils.text import slugify

SUBCATEGORY_MAP = {
    'matrimony': MATRIMONY_SUBCATEGORIES,
    'events': EVENTS_SUBCATEGORIES,
    'services': SERVICES_SUBCATEGORIES,
    'property': PROPERTY_SUBCATEGORIES,
    'automotive': CARS_SUBCATEGORIES,
    'items': ITEMS_SUBCATEGORIES,
    'jobs': JOBS_SUBCATEGORIES,
    'lifestyle': LIFESTYLE_SUBCATEGORIES,
    'travel': TRAVEL_SUBCATEGORIES,
    'wedding': WEDDING_SUBCATEGORIES,
}


class Command(BaseCommand):
    help = "Seed Categories and SubCategories"

    def handle(self, *args, **options):
        for name, display_name in CATEGORY_CHOICES:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'display_name': display_name,
                    'icon': f'{slugify(name)}.png',
                    'is_active': True,
                    'order': 0,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {display_name}"))

            subcategories = SUBCATEGORY_MAP.get(name, [])
            for sub_name, sub_display in subcategories:
                subcat, created = SubCategory.objects.get_or_create(
                    category=category,
                    name=sub_name,
                    defaults={
                        'display_name': sub_display,
                        'is_active': True,
                        'order': 0
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"  └─ Created subcategory: {sub_display}"))
