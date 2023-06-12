from rest_framework import serializers
from .models import User, Student, Mentor, Feedback, Topic, SubTopic
from .helphers import CITIES_CHOICES
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password')

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            hashed_password = make_password(password)
            instance.password = hashed_password
        return super().update(instance, validated_data)


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        sub_topics_data = validated_data.pop('sub_topics', None)
        user = User.objects.create_user(**user_data)  # Create a new User instance
        student = Student.objects.create(user=user, **validated_data)
        if sub_topics_data:
            student.sub_topics.add(*sub_topics_data)
        return student

    def update(self, instance, validated_data):
        user_data = self.context['user']
        if user_data:
            us = UserSerializer(instance=instance.user, data=user_data, partial=True)
            assert us.is_valid(), ValueError(us.errors)
            us.save()
        return super().update(instance, validated_data)


class MentorSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True)  # Embed the UserSerializer inside the StudentSerializer
    study_cities = serializers.MultipleChoiceField(choices=CITIES_CHOICES)
    class Meta:
        model = Mentor
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        sub_topics_data = validated_data.pop('sub_topics')
        user = User.objects.create_user(**user_data)  # Create a new User instance
        mentor = Mentor.objects.create(user=user, **validated_data)
        mentor.sub_topics.add(*sub_topics_data)
        return mentor

    def update(self, instance, validated_data):
        user_data = self.context['user']

        if user_data:
            us = UserSerializer(instance=instance.user, data=user_data, partial=True)
            assert us.is_valid(), ValueError(us.errors)
            us.save()
        return super().update(instance, validated_data)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
