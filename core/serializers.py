from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'password']

        def validate_email(self, value):
            if not value:
                raise serializers.ValidationError("Email is required")
            return value

        def create(self, validated_data):
            # Create the user with proper password handling using the custom manager
            user = User.objects.create_user(
                email=validated_data["email"], password=validated_data["password"]
            )
            return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError(_("Both email and password are required"))

        user = authenticate(
            request=self.context.get("request"),
            email=email,  # <- this is what Django expects
            password=password
        )

        if not user:
            raise serializers.ValidationError({"email": _("Invalid credentials")})

        if not user.is_active:
            raise serializers.ValidationError(_("User account is disabled"))

        data["user"] = user
        return data
