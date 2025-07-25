from django.db import models
from common.models import BaseModel
from core.models import User


class ChatRoom(BaseModel):
    """
    Chat room between two users
    """
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user1', 'user2']
        ordering = ['-created_at']

    def __str__(self):
        return f"Chat between {self.user1.name} and {self.user2.name}"

    @property
    def room_name(self):
        """Generate a unique room name for WebSocket"""
        user_ids = sorted([str(self.user1.id), str(self.user2.id)])
        return f"chat_{user_ids[0]}_{user_ids[1]}"

    @classmethod
    def get_or_create_room(cls, user1, user2):
        """Get or create a chat room between two users"""
        # Ensure consistent ordering to avoid duplicate rooms
        if str(user1.id) > str(user2.id):
            user1, user2 = user2, user1
        
        room, created = cls.objects.get_or_create(
            user1=user1,
            user2=user2,
            defaults={'is_active': True}
        )
        return room, created


class Message(BaseModel):
    """
    Individual message in a chat room
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text'),
            ('image', 'Image'),
            ('file', 'File'),
            ('system', 'System')
        ],
        default='text'
    )

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.name}: {self.content[:50]}..."

    def mark_as_read(self):
        """Mark message as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])


class OnlineUser(BaseModel):
    """
    Track online users for real-time features
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='online_status')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    socket_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.name} - {'Online' if self.is_online else 'Offline'}"

    @classmethod
    def set_user_online(cls, user, socket_id=None):
        """Set user as online"""
        online_user, created = cls.objects.get_or_create(
            user=user,
            defaults={'is_online': True, 'socket_id': socket_id}
        )
        if not created:
            online_user.is_online = True
            online_user.socket_id = socket_id
            online_user.save(update_fields=['is_online', 'socket_id', 'last_seen'])
        return online_user

    @classmethod
    def set_user_offline(cls, user):
        """Set user as offline"""
        try:
            online_user = cls.objects.get(user=user)
            online_user.is_online = False
            online_user.socket_id = None
            online_user.save(update_fields=['is_online', 'socket_id', 'last_seen'])
        except cls.DoesNotExist:
            pass


class Notification(BaseModel):
    """
    Real-time notifications for users
    """
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=50,
        choices=[
            ('connection_request', 'Connection Request'),
            ('connection_accepted', 'Connection Accepted'),
            ('new_message', 'New Message'),
            ('profile_view', 'Profile View'),
            ('ad_response', 'Ad Response'),
            ('system', 'System Notification')
        ]
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict, blank=True)  # Additional data for the notification

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.recipient.name}"

    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])