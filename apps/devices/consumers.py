import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class DeviceConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.group_name = f'device_{self.device_id}'

        # Join device group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'message': f'Connected to device {self.device_id}',
            'status': 'connected'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            status = data.get('status', 'offline')

            # Update device status in database
            await self.update_device_status(self.device_id, status)

            # Broadcast to group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'device_status',
                    'device_id': self.device_id,
                    'status': status,
                    'timestamp': timezone.now().isoformat()
                }
            )
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))

    async def device_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'device_id': event['device_id'],
            'status': event['status'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def update_device_status(self, device_id, status):
        from .models import Device
        try:
            device = Device.objects.get(device_id=device_id)
            device.status = status
            device.last_seen = timezone.now()
            device.save()
        except Device.DoesNotExist:
            pass