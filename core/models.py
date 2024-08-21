from datetime import timedelta
from django.utils import timezone
from common.models import BaseModel
from django.db import models
from django.contrib.auth.models import AbstractUser
from common.validators import validate_email_format, validate_phone_number
from .managers import CustomUserManager


class User(BaseModel, CustomUserManager):
    first_name = models.CharField(null=True, max_length=225)
    last_name = models.CharField(null=True, max_length=255)
    email = models.EmailField(unique=True, validators=[validate_email_format], null=True)
    country = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(unique=True, null=True, max_length=15, validators=[validate_phone_number])
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    class Meta:
        unique_together = ('email', 'phone_number')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class OTP(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp')
    code = models.PositiveIntegerField(null=True, max_length=4)
    verified = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True, auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.user.full_name} ----- {self.code}"

    def save( self, *args, **kwargs):
        if self.expiry_date is None:
            self.expiry_date = timezone.now() + timedelta(minutes=10)

        if timezone.now() > self.expiry_date:
            self.expired = True
        if self.expired:
            self.delete()

        super().save(*args, **kwargs)

