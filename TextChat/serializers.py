from rest_framework import serializers
from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('id',)


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
