from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
import logging

logger = logging.getLogger(__name__)


def send_notification_to_user(user, title, message, notification_type, data=None):
    """
    Send a real-time notification to a user
    """
    try:
        # Create notification in database
        notification = Notification.objects.create(
            recipient=user,
            title=title,
            message=message,
            notification_type=notification_type,
            data=data or {}
        )
        
        # Send real-time notification via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user.id}',
            {
                'type': 'send_notification',
                'notification_id': str(notification.id),
                'title': title,
                'message': message,
                'notification_type': notification_type,
                'timestamp': notification.created_at.isoformat(),
                'data': data or {}
            }
        )
        
        return notification
    except Exception as e:
        logger.error(f"Failed to send notification to user {user.id}: {str(e)}")
        return None


def send_connection_request_notification(sender, receiver):
    """Send notification when a connection request is sent"""
    return send_notification_to_user(
        user=receiver,
        title="New Connection Request",
        message=f"{sender.name} sent you a connection request",
        notification_type="connection_request",
        data={
            'sender_id': str(sender.id),
            'sender_name': sender.name
        }
    )


def send_connection_accepted_notification(sender, receiver):
    """Send notification when a connection request is accepted"""
    return send_notification_to_user(
        user=sender,
        title="Connection Request Accepted",
        message=f"{receiver.name} accepted your connection request",
        notification_type="connection_accepted",
        data={
            'receiver_id': str(receiver.id),
            'receiver_name': receiver.name
        }
    )


def send_new_message_notification(sender, receiver, message_content):
    """Send notification for new message"""
    return send_notification_to_user(
        user=receiver,
        title="New Message",
        message=f"{sender.name}: {message_content[:50]}{'...' if len(message_content) > 50 else ''}",
        notification_type="new_message",
        data={
            'sender_id': str(sender.id),
            'sender_name': sender.name,
            'message_preview': message_content[:100]
        }
    )


def send_profile_view_notification(viewer, profile_owner):
    """Send notification when someone views a profile"""
    return send_notification_to_user(
        user=profile_owner,
        title="Profile View",
        message=f"{viewer.name} viewed your profile",
        notification_type="profile_view",
        data={
            'viewer_id': str(viewer.id),
            'viewer_name': viewer.name
        }
    )