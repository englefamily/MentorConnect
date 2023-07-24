from rest_framework import serializers
from .models import Chat, Message
from mentorconnect import models as mc_models
from mentorconnect.serializers import StudentSerializer, MentorSerializer


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        student_fields=('id', 'first_name', 'last_name', 'phone_num')
        mentor_fields=('id', 'first_name', 'last_name', 'phone_num')
        student_serializer = StudentSerializer(instance.student.student).data
        mentor_serializer = MentorSerializer(instance.mentor.mentor).data
        representation['mentor'] = {key: value for key, value in mentor_serializer.items() if key in mentor_fields}
        representation['mentor']['user_id'] = instance.mentor.id

        representation['student'] = {key: value for key, value in student_serializer.items() if key in student_fields}
        representation['student']['user_id'] = instance.student.id

        return representation


class MessageSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ('email', 'message')

    def get_email(self, obj):
        return obj.user.email

    def get_message(self, obj):
        return obj.content
