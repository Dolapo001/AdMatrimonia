import random
from django.utils import timezone
from datetime import timedelta
#from core.models import OTP
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def generate_otp(user):
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
    numbers = ''.join(random.choices('0123456789', k=2))
    code = f"{letters}{numbers}"
    otp = OTP.objects.create(
        user=user,
        code=code,
        expiry_date=timezone.now() + timedelta(minutes=10)
    )
    send_otp_email(user.email, code)
    return otp


def send_otp_emai(email, code):
    pass


def verify_otp(user, code):
    otp = OTP.objects.filter(user=user, code=code, expired=False).first()
    if otp and timezone.now() <= otp.expiry_date:
        otp.verified = True
        otp.expired = True
        otp.save()
        return True
    return False
