# import logging
# import random
# from django.utils import timezone
# from datetime import timedelta
# from core.models import OTP
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings
#
# logger = logging.getLogger(__name__)
#
#
# def generate_otp(user):
#     letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
#     numbers = ''.join(random.choices('0123456789', k=2))
#     code = f"{letters}{numbers}"
#     otp = OTP.objects.create(
#         user=user,
#         code=code,
#         expiry_date=timezone.now() + timedelta(minutes=10)
#     )
#     send_otp_email(user.email, code)
#     return otp
#
#
# def send_otp_email(user, is_resend=False):
#     """Send OTP email for account verification or login."""
#     otp = generate_otp(user)
#     subject = "Your OTP Code" if not is_resend else "Resend OTP Code"
#     sender = settings.DEFAULT_FROM_EMAIL
#     recipient = [user.email]
#
#     context = {
#         "user_firstname": user.profile.first_name,
#         "otp_code": otp.code,
#         "expiry_time": "10 minutes",
#         "email_sender_name": settings.EMAIL_SENDER_NAME,
#     }
#
#     email_html_message = render_to_string("otp_email.html", context)
#     email_plain_message = render_to_string("otp_email.txt", context)
#
#     try:
#         msg = EmailMultiAlternatives(subject, email_plain_message, sender, recipient)
#         msg.attach_alternative(email_html_message, "text/html")
#         msg.send()
#         logger.info(f"OTP email sent successfully to {user.email}")
#     except Exception as e:
#         logger.error(f"Failed to send OTP email to {user.email}: {str(e)}")
#
#     return otp
#
#
#
# def send_otp_emai(email, code):
#     pass
#
#
# def verify_otp(user, code):
#     otp = OTP.objects.filter(user=user, code=code, expired=False).first()
#     if otp and timezone.now() <= otp.expiry_date:
#         otp.verified = True
#         otp.expired = True
#         otp.save()
#         return True
#     return False
