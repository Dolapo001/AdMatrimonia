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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class ConnectionRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = ConnectionRequest
        fields = ['id', 'sender', 'receiver', 'status', 'message']


class SendConnectionRequestSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()
    message = serializers.CharField(required=False, allow_blank=True)


class RespondConnectionRequestSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=[('accepted', 'Accepted'), ('rejected', 'Rejected')])


class BookmarkSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'profile']
