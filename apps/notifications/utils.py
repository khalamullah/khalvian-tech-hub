from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def send_notification(user, message, notification_type='info'):
    """
    Creates a notification in the database and pushes it
    to the user's browser in real-time via WebSocket.
    """
    # Save to database
    notification = Notification.objects.create(
        user=user,
        message=message,
        notification_type=notification_type
    )

    # Push to WebSocket
    channel_layer = get_channel_layer()
    group_name = f'notifications_{user.id}'

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'message': message,
            'notification_type': notification_type,
            'created_at': notification.created_at.isoformat()
        }
    )

    return notification