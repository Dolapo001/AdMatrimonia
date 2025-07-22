from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from .emails import *


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required")
        return value

    def create(self, validated_data):
        import uuid

        validated_data["username"] = str(uuid.uuid4())[:30]  # ✨ random dummy username

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data["username"],
            phone_number=validated_data.get("phone_number"),
            name=validated_data.get("name")
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError({"email": "Invalid credentials"})

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data["user"] = user
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    identifier = serializers.EmailField()

    def validate(self, data):
        identifier = data.get("identifier")
        user = User.objects.filter(email=identifier).first()
        if not user:
            raise serializers.ValidationError(_("User not found"))
        data["user"] = user
        return data


class ResetPasswordSerializer(serializers.Serializer):
    identifier = serializers.EmailField()  # Use EmailField for validation
    code = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(_("Passwords do not match"))

        # Query only by email since phone verification is not supported.
        user = User.objects.filter(email=data["identifier"]).first()
        if not user:
            raise serializers.ValidationError(_("User not found"))

        # Verify OTP using the provided code
        if not verify_otp(user, data["code"]):
            raise serializers.ValidationError(_("Invalid OTP or OTP has expired"))

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


