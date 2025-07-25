from django.urls import path
from .views import (
    ChatRoomListView,
    CreateChatRoomView,
    ChatRoomMessagesView,
    NotificationListView,
    MarkNotificationReadView,
    UnreadNotificationsCountView
)

urlpatterns = [
    # Chat rooms
    path('rooms/', ChatRoomListView.as_view(), name='chat-room-list'),
    path('rooms/create/', CreateChatRoomView.as_view(), name='create-chat-room'),
    path('rooms/<str:room_id>/messages/', ChatRoomMessagesView.as_view(), name='chat-room-messages'),
    
    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<str:notification_id>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('notifications/unread-count/', UnreadNotificationsCountView.as_view(), name='unread-notifications-count'),
]