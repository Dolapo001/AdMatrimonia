from rest_framework import serializers
from .models import MatrimonyProfile, MatrimonyProfilePicture


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
