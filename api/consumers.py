import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the order ID from the URL and join a group specific to that order
        self.pk = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'order_{self.pk}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group when the connection is closed
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Not used in this example, but you can handle client messages here if needed
        pass

    async def notify_order_status(self, event):
        print(event,"status")
        # Send the order status update to the client
        status = event['status']
        await self.send(text_data=json.dumps({
            'status': status,
            'event': event,
        }))
