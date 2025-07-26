from django.contrib import admin
from .models import ChatRoom, Message, OnlineUser, Notification


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'user1', 'user2', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user1__name', 'user2__name', 'user1__email', 'user2__email']
    readonly_fields = ['created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'room', 'content_preview', 'timestamp', 'is_read', 'message_type']
    list_filter = ['message_type', 'is_read', 'timestamp']
    search_fields = ['sender__name', 'content']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(OnlineUser)
class OnlineUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_online', 'last_seen', 'socket_id']
    list_filter = ['is_online', 'last_seen']
    search_fields = ['user__name', 'user__email']
    readonly_fields = ['last_seen']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipient', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__name', 'title', 'message']
    readonly_fields = ['created_at']