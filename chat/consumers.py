import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from core.models import User
from .models import ChatRoom, Message, OnlineUser, Notification

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = self.scope["user"]
        
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Verify user has access to this room
        has_access = await self.verify_room_access()
        if not has_access:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Set user as online
        await self.set_user_online()

        await self.accept()

        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to chat room'
        }))

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'room_group_name'):
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

        # Set user as offline
        if hasattr(self, 'user') and not isinstance(self.user, AnonymousUser):
            await self.set_user_offline()

    async def receive(self, text_data):
        """Handle messages from WebSocket"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'chat_message')

            if message_type == 'chat_message':
                await self.handle_chat_message(text_data_json)
            elif message_type == 'typing':
                await self.handle_typing(text_data_json)
            elif message_type == 'mark_read':
                await self.handle_mark_read(text_data_json)

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error in receive: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'An error occurred'
            }))

    async def handle_chat_message(self, data):
        """Handle chat message"""
        message_content = data.get('message', '').strip()
        if not message_content:
            return

        # Save message to database
        message = await self.save_message(message_content)
        if not message:
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender_id': str(self.user.id),
                'sender_name': self.user.name,
                'timestamp': message['timestamp'],
                'message_id': str(message['id'])
            }
        )

    async def handle_typing(self, data):
        """Handle typing indicator"""
        is_typing = data.get('is_typing', False)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user_id': str(self.user.id),
                'user_name': self.user.name,
                'is_typing': is_typing
            }
        )

    async def handle_mark_read(self, data):
        """Handle mark messages as read"""
        message_ids = data.get('message_ids', [])
        await self.mark_messages_read(message_ids)

    # WebSocket message handlers
    async def chat_message(self, event):
        """Send chat message to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id']
        }))

    async def typing_indicator(self, event):
        """Send typing indicator to WebSocket"""
        # Don't send typing indicator to the sender
        if event['user_id'] != str(self.user.id):
            await self.send(text_data=json.dumps({
                'type': 'typing_indicator',
                'user_id': event['user_id'],
                'user_name': event['user_name'],
                'is_typing': event['is_typing']
            }))

    # Database operations
    @database_sync_to_async
    def verify_room_access(self):
        """Verify user has access to the chat room"""
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            return self.user == room.user1 or self.user == room.user2
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content):
        """Save message to database"""
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            message = Message.objects.create(
                room=room,
                sender=self.user,
                content=content
            )
            return {
                'id': message.id,
                'timestamp': message.timestamp.isoformat()
            }
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")
            return None

    @database_sync_to_async
    def mark_messages_read(self, message_ids):
        """Mark messages as read"""
        try:
            Message.objects.filter(
                id__in=message_ids,
                room__id=self.room_id
            ).exclude(sender=self.user).update(is_read=True)
        except Exception as e:
            logger.error(f"Error marking messages as read: {str(e)}")

    @database_sync_to_async
    def set_user_online(self):
        """Set user as online"""
        try:
            OnlineUser.set_user_online(self.user, self.channel_name)
        except Exception as e:
            logger.error(f"Error setting user online: {str(e)}")

    @database_sync_to_async
    def set_user_offline(self):
        """Set user as offline"""
        try:
            OnlineUser.set_user_offline(self.user)
        except Exception as e:
            logger.error(f"Error setting user offline: {str(e)}")


class NotificationConsumer(AsyncWebsocketConsumer):
    """Consumer for real-time notifications"""
    
    async def connect(self):
        """Handle WebSocket connection for notifications"""
        self.user = self.scope["user"]
        
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        self.notification_group_name = f'notifications_{self.user.id}'

        # Join notification group
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )

        await self.accept()

        # Send unread notifications count
        unread_count = await self.get_unread_notifications_count()
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': unread_count
        }))

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'notification_group_name'):
            await self.channel_layer.group_discard(
                self.notification_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """Handle messages from WebSocket"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            if message_type == 'mark_notification_read':
                notification_id = text_data_json.get('notification_id')
                await self.mark_notification_read(notification_id)

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))

    # WebSocket message handlers
    async def send_notification(self, event):
        """Send notification to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'id': event['notification_id'],
            'title': event['title'],
            'message': event['message'],
            'notification_type': event['notification_type'],
            'timestamp': event['timestamp'],
            'data': event.get('data', {})
        }))

    # Database operations
    @database_sync_to_async
    def get_unread_notifications_count(self):
        """Get count of unread notifications"""
        try:
            return Notification.objects.filter(
                recipient=self.user,
                is_read=False
            ).count()
        except Exception as e:
            logger.error(f"Error getting unread notifications count: {str(e)}")
            return 0

    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient=self.user
            )
            notification.mark_as_read()
        except Notification.DoesNotExist:
            pass
        except Exception as e:
            logger.error(f"Error marking notification as read: {str(e)}")