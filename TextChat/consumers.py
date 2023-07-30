import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from mentorconnect.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_group_name = self.scope['url_route']['kwargs']['chat_id']

        print(self.chat_group_name)
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    # async def send_history_chat(self, chat_group_name):
    #     chat = await database_sync_to_async(Chat.objects.get)(pk='2-5')
    #     messages = await database_sync_to_async(Message.objects.filter)(chat=chat)
    #     serialized_messages = await self.serialize_messages(messages)
    #     await self.send(text_data=serialized_messages)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )
        await super().disconnect(code)

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)
        print("**************************")
        print(data)
        # message = data['message']
        # email = data['email']
        # chat_id = data['chat_id']

        await self.save_message(data['email'], data['chat_id'], data['message'])

        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": 'chat_message',
                "message": data['message'],
                "email": data['email']
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        email = event['email']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "email": email
        }))


    # async def send_history_chat(self, chat_id):
    #     messages = Message.objects.filter(chat_id=chat_id)
    #
    #     serialized_messages = MessageSerializers(messages, many=True).data
    #     await self.send(text_data=serialized_messages)

    @sync_to_async
    def save_message(self, email, chat_id, message):
        user = User.objects.get(email=email)
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            print('create')
            chat = Chat.objects.create(id=chat_id)
        Message.objects.create(user=user, chat=chat, content=message)

    # async def serialize_messages(self, messages):
    #     # Serialize messages asynchronously
    #     serializer = MessageSerializer(messages, many=True)
    #     serialized_data = serializer.data
    #     return json.dumps(serialized_data)
