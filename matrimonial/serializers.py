from rest_framework import serializers
from .models import MatrimonyProfile, MatrimonyProfilePicture


class MatrimonyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrimonyProfile
        exclude = ('created_at', 'updated_at')

