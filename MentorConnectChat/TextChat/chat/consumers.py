import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # TODO: Create ability to use `Username` (eg Mentor) as the Room Name (Channel names are created automatically per user)
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        # TODO: Create ability to add user (channel name) to the messages so can see how said what...
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))