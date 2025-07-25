from rest_framework import serializers
from .models import ChatRoom, Message, Notification
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'timestamp', 'is_read', 'message_type']


class ChatRoomSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'user1', 'user2', 'created_at', 'is_active', 'room_name', 'last_message', 'unread_count']
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
    def get_unread_count(self, obj):
        request_user = self.context.get('request').user if self.context.get('request') else None
        if request_user:
            return obj.messages.filter(is_read=False).exclude(sender=request_user).count()
        return 0


class CreateChatRoomSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    
    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'is_read', 'created_at', 'data']