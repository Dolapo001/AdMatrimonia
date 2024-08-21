from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from core.emails import verify_otp
from core.models import User


def validate_email_format(value):
    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError("Invalid email format")


def validate_otp(user, otp_code):
    if not verify_otp(user, otp_code):
        raise ValidationError("Invalid or expired OTP")
    return True


def validate_phone_number(value):
    if not value.startwith('+'):
        raise ValidationError("Phone number must start with as plus sign (+)")
    if not value[1:].isdigit():
        raise ValidationError("Phone number must only contain digits after the plus sign (+)")


def validate_image_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError("Image size should be less than 5MB")


def validate_date(value):
    if value is not None and value > timezone.now().date():
        raise ValidationError("Birthday must be in the past.")


def validate_old_password(user, old_password):
    if not user.check_password(old_password):
        raise ValidationError("Old password is incorrect")
    return True
