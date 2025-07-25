from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import ChatRoom, Message, Notification
from .serializers import ChatRoomSerializer, MessageSerializer, CreateChatRoomSerializer, NotificationSerializer
from common.response_managers import ResponseManager, ResponseStatus
import logging

logger = logging.getLogger(__name__)


class ChatRoomListView(APIView):
    """List all chat rooms for the authenticated user"""
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get(self, request):
        try:
            chat_rooms = ChatRoom.objects.filter(
                Q(user1=request.user) | Q(user2=request.user),
                is_active=True
            ).order_by('-created_at')

            serializer = self.serializer_class(chat_rooms, many=True, context={'request': request})
            return ResponseManager.success_response(
                message="Chat rooms fetched successfully",
                data={"chat_rooms": serializer.data}
            )
        except Exception as e:
            logger.exception("Failed to fetch chat rooms")
            return ResponseManager.server_error_response(
                message="Failed to fetch chat rooms",
                error=str(e)
            )


class CreateChatRoomView(APIView):
    """Create or get existing chat room with another user"""
    permission_classes = [IsAuthenticated]
    serializer_class = CreateChatRoomSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return ResponseManager.validation_error_response(
                    errors=serializer.errors
                )

            other_user = serializer.validated_data['user_id']
            
            if other_user == request.user:
                return ResponseManager.validation_error_response(
                    message="Cannot create chat room with yourself"
                )

            room, created = ChatRoom.get_or_create_room(request.user, other_user)
            
            room_serializer = ChatRoomSerializer(room, context={'request': request})
            
            status_message = "Chat room created successfully" if created else "Chat room already exists"
            return ResponseManager.success_response(
                message=status_message,
                data=room_serializer.data
            )
        except Exception as e:
            logger.exception("Failed to create chat room")
            return ResponseManager.server_error_response(
                message="Failed to create chat room",
                error=str(e)
            )


class ChatRoomMessagesView(APIView):
    """Get messages for a specific chat room"""
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, room_id):
        try:
            # Verify user has access to this room
            try:
                room = ChatRoom.objects.get(
                    id=room_id,
                    is_active=True
                )
                if request.user not in [room.user1, room.user2]:
                    return ResponseManager.forbidden_response(
                        message="You don't have access to this chat room"
                    )
            except ChatRoom.DoesNotExist:
                return ResponseManager.not_found_response("Chat room not found")

            # Get messages
            messages = Message.objects.filter(room=room).order_by('timestamp')
            
            # Mark messages as read (except sender's own messages)
            Message.objects.filter(
                room=room,
                is_read=False
            ).exclude(sender=request.user).update(is_read=True)

            return ResponseManager.custom_paginated_response(
                request,
                messages,
                self.serializer_class,
                message="Messages fetched successfully"
            )
        except Exception as e:
            logger.exception(f"Failed to fetch messages for room {room_id}")
            return ResponseManager.server_error_response(
                message="Failed to fetch messages",
                error=str(e)
            )


class NotificationListView(APIView):
    """List notifications for the authenticated user"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get(self, request):
        try:
            notifications = Notification.objects.filter(
                recipient=request.user
            ).order_by('-created_at')

            return ResponseManager.custom_paginated_response(
                request,
                notifications,
                self.serializer_class,
                message="Notifications fetched successfully"
            )
        except Exception as e:
            logger.exception("Failed to fetch notifications")
            return ResponseManager.server_error_response(
                message="Failed to fetch notifications",
                error=str(e)
            )


class MarkNotificationReadView(APIView):
    """Mark notification as read"""
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            try:
                notification = Notification.objects.get(
                    id=notification_id,
                    recipient=request.user
                )
                notification.mark_as_read()
                return ResponseManager.success_response(
                    message="Notification marked as read"
                )
            except Notification.DoesNotExist:
                return ResponseManager.not_found_response("Notification not found")
        except Exception as e:
            logger.exception(f"Failed to mark notification {notification_id} as read")
            return ResponseManager.server_error_response(
                message="Failed to mark notification as read",
                error=str(e)
            )


class UnreadNotificationsCountView(APIView):
    """Get count of unread notifications"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            count = Notification.objects.filter(
                recipient=request.user,
                is_read=False
            ).count()
            
            return ResponseManager.success_response(
                message="Unread notifications count fetched successfully",
                data={"unread_count": count}
            )
        except Exception as e:
            logger.exception("Failed to fetch unread notifications count")
            return ResponseManager.server_error_response(
                message="Failed to fetch unread notifications count",
                error=str(e)
            )