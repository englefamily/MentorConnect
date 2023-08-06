from rest_framework import serializers
from .models import User, Student, Mentor, Feedback, Topic, StudySession, StudySessionSlot
from .helphers import CITIES_CHOICES, EXPERIENCE_CHOICES
from django.contrib.auth.hashers import make_password
from datetime import datetime, time
from collections import OrderedDict
from TextChat import models as tc_models
from datetime import datetime
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'id')

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            hashed_password = make_password(password)
            instance.password = hashed_password
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            hashed_password = make_password(password)
            validated_data['password'] = hashed_password
        
        return super().create(validated_data)
    



class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True)

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        topics_data = validated_data.pop('topics', None)
        user = User.objects.create_user(**user_data)  # Create a new User instance
        student = Student.objects.create(user=user, **validated_data)
        if topics_data:
            student.topics.add(*topics_data)
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if user_data.get('email'):
            instance.user.email = user_data.get('email')
            instance.user.save()
        return super().update(instance, validated_data)


class MentorSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True)  # Embed the UserSerializer inside the StudentSerializer
    study_cities = serializers.MultipleChoiceField(choices=CITIES_CHOICES)
    experience_with = serializers.MultipleChoiceField(choices=EXPERIENCE_CHOICES)
    rating = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()

    class Meta:
        model = Mentor
        fields = '__all__'


    def get_rating(self, obj):
        feedbacks = obj.feedbacks.all()
        total_stars = sum(feedback.stars for feedback in feedbacks)
        if feedbacks.exists():
            average_rating = total_stars / feedbacks.count()
            return {'avg': average_rating, 'count_rating': len(feedbacks)}
        return {'avg': 0, 'count_rating': 0}
    
    def get_price_range(self, obj):
        min_price = min(filter(lambda x: True if x != 0 else False ,[obj.teach_online, obj.teach_at_student, obj.teach_at_mentor]))
        max_price = max(filter(lambda x: True if x != 0 else False ,[obj.teach_online, obj.teach_at_student, obj.teach_at_mentor]))
        if min_price == max_price:
            return min_price
        
        return f'{min_price}-{max_price}'
        



    def to_representation(self, instance):
        # Modify the serialized response here
        representation = super().to_representation(instance)
        representation['topics'] = [TopicSerializer(Topic.objects.get(id=id)).data for id in representation['topics']]
        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        topics_data = validated_data.pop('topics')

        try:
            with transaction.atomic():
                user = User.objects.create_user(**user_data)  # Create a new User instance
                mentor = Mentor.objects.create(user=user, **validated_data)

                student_data = {
                    'user': user,
                    'first_name': validated_data['first_name'],
                    'last_name': validated_data['last_name'],
                    'phone_num': validated_data['phone_num'],
                    # Add other student data here
                }
                student = Student.objects.create(**student_data)

                mentor.topics.add(*topics_data)

                return mentor

        except Exception as e:
            # If an exception occurs, the transaction will be rolled back, and no objects will be created.
            # You can add any handling you need for the exception here.
            print(f"Error: {e}")
            raise e


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if user_data.get('email'):
            instance.user.email = user_data.get('email')
            instance.user.save()
        return super().update(instance, validated_data)

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class StudySessionSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySessionSlot
        fields = '__all__'


class StudySessionSerializer(serializers.ModelSerializer):
    slot = StudySessionSlotSerializer(partial=True)
    topic_name = serializers.SerializerMethodField()
    mentor_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    date_passed = serializers.SerializerMethodField()

    class Meta:
        model = StudySession
        fields = '__all__'

    def get_topic_name(self, obj):
        return obj.topic.name
    
    def get_student_name(self, obj):
        return f'{obj.student.first_name} {obj.student.last_name}'
    
    def get_mentor_name(self, obj):
        return f'{obj.slot.mentor.first_name} {obj.slot.mentor.last_name}'
    
    def get_date_passed(self, obj):
        target_datetime_str = f"{obj.slot.date}, {obj.slot.end_time}"
        target_datetime_obj = datetime.strptime(target_datetime_str, "%Y-%m-%d, %H:%M:%S")

        # Get the current datetime
        current_datetime_obj = datetime.now()

        # Compare the target datetime with the current datetime
        if current_datetime_obj >= target_datetime_obj:
            return True
        else:
            return False

    

    def to_representation(self, instance):
        # Modify the serialized response here
        representation = super().to_representation(instance)
        teach_method = instance.teach_method
        representation['hourly_rate'] = getattr(instance.slot.mentor, f'teach_{instance.teach_method}')
        
        
        return representation
    
    def create(self, validated_data):
        slot_data = validated_data.pop('slot')
        slot = StudySessionSlot.objects.create(**slot_data)  # Create a new User instance
        study_session = StudySession.objects.create(slot=slot, **validated_data)
        return study_session

    def update(self, instance, validated_data):
        slot_data = validated_data.pop('slot', {})
        if slot_data:
            
            data = OrderedDict([
                ('id', 1),
                ('date', slot_data['date']),
                ('start_time', slot_data['start_time']),
                ('end_time', slot_data['end_time']),
                ('mentor', 1)
            ])
            slot_serializer = StudySessionSlotSerializer(instance.slot, data=data)
            if slot_serializer.is_valid():
                slot_serializer.save()
        return super().update(instance, validated_data)


class StudentsFromChatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = tc_models.Chat
        fields = '__all__'

    def to_representation(self, instance):
        # Modify the serialized response here
        representation = super().to_representation(instance)
        # representation = []
        representation['first_name'] = instance.student.student.first_name
        representation['last_name'] = instance.student.student.last_name
        representation['id'] = instance.student.student.id
        
        
        return representation

    


