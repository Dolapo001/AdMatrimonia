from rest_framework import serializers
from .models import *


class MatrimonyProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrimonyProfilePicture
        fields = ['id', 'image']


class MatrimonyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrimonyProfile
        exclude = ('created_at', 'updated_at')


class MatrimonyProfileDetailSerializer(serializers.ModelSerializer):
    pictures = MatrimonyProfilePictureSerializer(many=True, read_only=True)

    class Meta:
        model = MatrimonyProfile
        fields = (
            'id',
            'pictures',
            'height',
            'expectations',
            'education',
            'address',
            'profession'
        )


class PartnerPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerPreference
        fields = ['min_age', 'max_age', 'min_height', 'max_height', 'caste', 'education']