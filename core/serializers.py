from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


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



