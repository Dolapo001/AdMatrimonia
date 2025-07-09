from django.db import models
from common.models import BaseModel
from core.models import User

gender_choice = [
    ('female', 'Female'),
    ('male', 'Male'),
    ('other', 'Male')
]


class MatrimonyProfile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matrimony_profile'),
    gender = models.CharField(choices=gender_choice, null=True, blank=True, max_length=10)
    height = models.CharField(max_length=20, null=True, blank=True),
    birthdate = models.DateField(null=True, blank=True),
    religion = models.CharField(max_length=20, null=True, blank=True),
    address = models.CharField(max_length=20, null=True, blank=True),
    education = models.CharField(max_length=20, null=True, blank=True),
    profession = models.CharField(max_length=20, null=True, blank=True),
    income = models.CharField(max_length=20, null=True, blank=True),
    bio = models.TextField(null=True, blank=True)
    expectations = models.CharField(max_length=250, null=True, blank=True),

    def __str__(self):
        return f"{self.user.name()} Matrimony Profile"



