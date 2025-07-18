from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import uuid
from common.models import BaseModel
from core.models import User
from .constants import *
from .query_managers import *
from .utils import generate_unique_publik_id


class Category(BaseModel):
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100) # use clodinary to store
    color = models.CharField(max_length=7, default='#000000') #might remove
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    objects = CategoryManager()

    class Meta:
        ordering = ['order', 'display_name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.display_name


class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100, choices=ALL_SUBCATEGORIES)
    display_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = SubCategoryManager()

    class Meta:
        ordering = ['order', 'display_name']
        unique_together = ['category', 'name']

    def __str__(self):
        return f"{self.category.display_name} - {self.display_name}"


class Ad(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='GBP')
    location = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    images = models.JSONField(default=list, blank=True)  # Store image URLs
    status = models.CharField(max_length=20, choices=Ad_Status, default='pending')
    is_featured = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    publik_id = models.CharField(max_length=20, unique=True, blank=True)
    objects = AdManager()
    pending_since = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.category.display_name}"

    def clean(self):
        super().clean()
        now = timezone.now()
        if self.expires_at:
            if self.expires_at < now:
                raise ValidationError("Expiration date must be in the future.")
            if self.expires_at > now + timedelta(days=60):
                raise ValidationError("Expiration date cannot be more than 60 days from now.")
            if self.expires_at < now + timedelta(days=1):
                raise ValidationError("Ad must be active for at least 1 day.")

    def save(self, *args, **kwargs):
        # Generate public_id only on creation
        if not self.publik_id:
            if hasattr(self.category, 'slug'):
                category_slug = self.category.slug
            else:
                category_slug = slugify(str(self.category))
            self.publik_id = generate_unique_publik_id(category_slug)

        # Default expire in 30 days if not provided
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)

        if self.status == 'pending' and not self.pending_since:
            self.pending_since = timezone.now()
            self.full_clean()
        super().save(*args, **kwargs)


class FavoriteAd(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_ads')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = FavoriteAdManager()

    class Meta:
        unique_together = ['user', 'ad']

    def __str__(self):
        return f"{self.user.name} - {self.ad.title}"

    def clean(self):
        try:
            uuid.UUID(str(self.ad_id))
            uuid.UUID(str(self.user_id))
        except ValueError:
            raise ValidationError("Invalid UUID format")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SearchHistory(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']
