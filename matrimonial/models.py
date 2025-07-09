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
        return f"{self.user.name} Matrimony Profile"


class MatrimonyProfilePicture(BaseModel):
    profile = models.ForeignKey(MatrimonyProfile, on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to='matrimony/profile_pics/')

    def __str__(self):
        return f"Picture of {self.profile.user.name}"


class PartnerPreference(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner_preference')
    min_age = models.PositiveIntegerField(null=True, blank=True)
    max_age = models.PositiveIntegerField(null=True, blank=True)

    min_height = models.CharField(max_length=10, null=True, blank=True)
    max_height = models.CharField(max_length=10, null=True, blank=True)

    caste = models.CharField(max_length=50, null=True, blank=True)
    education = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Partner Preferences of {self.user.name}"


class ConnectionRequest(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    message = models.TextField(null=True, blank=True)
    is_bookmarked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"


class Bookmark(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    profile = models.ForeignKey(MatrimonyProfile, on_delete=models.CASCADE, related_name='bookmarked_by')
