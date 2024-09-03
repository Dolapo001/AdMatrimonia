from rest_framework import serializers
from .models import User


class RegisterUser(serializers.ModelSerializer):
    model = User
    fields = ['fir']