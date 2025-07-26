from django.urls import path
from .views import *





urlpatterns = [
    path("register/", RegistrationView.as_view(), name="sign-up"),
    path("login/", LoginView.as_view(), name="sign-in"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
]
