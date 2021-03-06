import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'Connected from django Channels hello'}))
        print("GroupName: ", self.room_group_name)
        print("room_name", self.room_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        lat = data['latitude']
        long = data['longitude']

        await self.channel_layer.group_send(self.room_name, {
            'type': "location",
            'latitude': lat,
            'longitude': long,
        })

    async def location(self, event):
        lat = event['latitude']
        long = event['longitude']
        await self.send(text_data=json.dumps(
            {
                'latitude': lat,
                'longitude': long,

            }
        )
        )

    async def disconnect(self, close_code):
        print("Disconnect")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
