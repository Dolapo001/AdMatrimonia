from django.db import models
from common.models import BaseModel
from .constants import *


class Category(BaseModel):
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100) # use clodinary to store
    color = models.CharField(max_length=7, default='#000000') #might remove
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'display_name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.display_name


class