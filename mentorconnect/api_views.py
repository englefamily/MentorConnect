from .models import User, Student, Mentor, Topic, Feedback, StudySessionSlot, StudySession
from .forms import RegistrationForm, LoginForm
from .serializers import MentorSerializer, StudentSerializer, TopicSerializer, FeedbackSerializer, \
    StudySessionSlotSerializer, StudySessionSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache
# from django.core.exceptions import
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Count, Q
import jwt
from django.conf import settings
from rest_framework.exceptions import ValidationError


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        userType = []
        try:
            user.mentor
            userType += ['mentor']
        except Exception as error:
            print(error)

        try:
            user.student
            userType += ['student']
        except Exception as error:
            print(error)

        print(userType)
        token['email'] = user.email
        if 'mentor' in userType:
            token['first_name'] = user.mentor.first_name
            token['last_name'] = user.mentor.last_name
        elif 'student' in userType:
            token['first_name'] = user.student.first_name
            token['last_name'] = user.student.last_name
        token['type'] = userType


        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def mentor(request):
    try:
        match request.method:
            case 'POST':
                new_mentor = MentorSerializer(data=request.data)
                if new_mentor.is_valid():
                    mentor = new_mentor.save()
                    token, _ = Token.objects.get_or_create(user=mentor.user)
                    return Response(
                        status=status.HTTP_201_CREATED,
                        data={
                            "status": 'success',
                            'message': 'Mentor profile created',
                            'token': token.key,
                            'mentor': new_mentor.data
                        }
                    )
                else:
                    print(new_mentor.errors)
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'the data provided is incorrect',
                            'error': new_mentor.errors
                        }
                    )
            case 'GET':
                # todo add order by lisense and stars
                user_token = request.query_params.get("token")
                topics_param = request.query_params.get("topics")
                cities_param = request.query_params.get("cities")

                mentors = Mentor.objects

                if request.query_params:

                    if cities_param:
                        cities_lst = cities_param.split(',')
                        conditions = Q()
                        for city in cities_lst:
                            conditions |= Q(study_cities__contains=city)
                        mentors = mentors.filter(conditions) \
                            .annotate(num_matches=Count('study_cities')) \
                            .order_by('-num_matches')

                    if topics_param:
                        topics_set = set(topics_param.split(','))
                        mentors = mentors.filter(topics__id__in=topics_set) \
                            .annotate(match_count=Count('topics')) \
                            .order_by('-match_count')

                    if user_token:
                        try:
                            decoded_token = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
                            mentor = User.objects.get(id=decoded_token['user_id']).mentor
                        except Exception as error:
                            print(error)
                            return Response(
                                status=status.HTTP_400_BAD_REQUEST,
                                data={
                                    'status': 'fail',
                                    'message': f'token not valid'
                                }
                            )
                        mentor_json = MentorSerializer(mentor)
                        return Response(
                            status=status.HTTP_200_OK,
                            data={
                                'status': 'success',
                                'message': 'user found',
                                'mentor': mentor_json.data  # convert to JSON compatible format
                            }
                        )
                else:
                    mentors = mentors.all()

                mentors_json = MentorSerializer(mentors, many=True)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'retrieved all mentors',
                        'mentors': mentors_json.data  # convert to JSON compatible format
                    }
                )


            case 'PUT':
                user_token = request.data.get('token')
                if not user_token:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'Token not provided'
                        }
                    )

                try:
                    decoded_token = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
                    mentor_instance = User.objects.get(id=decoded_token['user_id']).mentor
                except (jwt.DecodeError, User.DoesNotExist) as error:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'Invalid token'
                        }
                    )

                mentor_data = request.data
                mentor_data.pop('token')
                if mentor_data.get('user', {}).get('email') == mentor_instance.user.email:
                    mentor_data['user'].pop('email')

                ms = MentorSerializer(instance=mentor_instance, data=mentor_data, partial=True)
                try:
                    ms.is_valid(raise_exception=True)
                    ms.save()
                except ValidationError as error:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'Invalid data',
                            'errors': error.detail
                        }
                    )
                except ValueError as error:
                    return Response(
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={
                            'status': 'error',
                            'message': str(error)
                        }
                    )

                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'Mentor updated',
                        'mentor': ms.data
                    }
                )

            case 'DELETE':
                user_token = request.query_params.get("token")
                user_instance = User.objects.get(pk=user_token)
                user_instance.delete()
                return Response("Mentor Deleted")

            case _:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'status': 'fail',
                        'message': f'the method {request.method} is not allowed for this url'
                    }
                )

    except Exception as ex:
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'status': 'fail',
                'message': 'a server error was thrown',
                'error': str(ex) # convert to string to make it JSON serializable
            }
        )


# Let's update below `student` `GET` method to include search by criteria
# (sub_topic, city, hourly rate, time, topic, feedback) and return list of mentors that meet the criteria

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def student(request):
    # try:
    if True:
        match request.method:
            case 'POST':
                new_student = StudentSerializer(data=request.data)
                if new_student.is_valid():
                    student = new_student.save()
                    token, _ = Token.objects.get_or_create(user=student.user)
                    return Response(
                        status=status.HTTP_201_CREATED,
                        data={
                            "status": 'success',
                            'message': 'Student profile created',
                            'token': token.key,
                            'student': new_student.data
                        }
                    )
                else:
                    print(new_student.errors)
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'the data provided is incorrect',
                            'error': new_student.errors
                        }
                    )
            case 'GET':
                user_token = request.query_params.get("token")

                students = Student.objects

                if user_token:
                    try:
                        decoded_token = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
                        student = Student.objects.get(
                            user__id=decoded_token['user_id'])  # Retrieve the Student instance
                        print(student.user)
                    except Exception as error:
                        print(error)
                        return Response(
                            status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'status': 'fail',
                                'message': f'token not valid'
                            }
                        )
                    student_serializer = StudentSerializer(student)  # Serialize the Student instance
                    print(student_serializer.data)
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            'status': 'success',
                            'message': 'user found',
                            'student': student_serializer.data  # Convert to JSON compatible format
                        }
                    )
                else:
                    students = students.all()

                students_serializer = StudentSerializer(students, many=True)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'retrieved all students',
                        'students': students_serializer.data  # Convert to JSON compatible format
                    }
                )
            case 'GET':
                user_token = request.query_params.get("token")

                students = Student.objects

                if user_token:
                    try:
                        decoded_token = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
                        student = Student.objects.get(
                            user__id=decoded_token['user_id'])  # Retrieve the Student instance
                        print(student.user)
                    except Exception as error:
                        print(error)
                        return Response(
                            status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'status': 'fail',
                                'message': f'token not valid'
                            }
                        )
                    student_serializer = StudentSerializer(student)  # Serialize the Student instance
                    print(student_serializer.data)
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            'status': 'success',
                            'message': 'user found',
                            'student': student_serializer.data  # Convert to JSON compatible format
                        }
                    )
                else:
                    students = students.all()

                students_serializer = StudentSerializer(students, many=True)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'retrieved all students',
                        'students': students_serializer.data  # Convert to JSON compatible format
                    }
                )

            case 'PUT':
                user_token = request.data.get('token')
                if not user_token:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'Token not provided'
                        }
                    )

                try:
                    decoded_token = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
                    student_instance = Student.objects.get(
                        user__id=decoded_token['user_id'])  # Retrieve the Student instance
                except Exception as error:
                    print(error)
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': f'token not valid'
                        }
                    )

                student_data = request.data
                student_data.pop('token')
                if student_data.get('user', {}).get('email') == student_instance.user.email:
                    student_data['user'].pop('email')

                student_serializer = StudentSerializer(instance=student_instance, data=student_data, partial=True)
                try:
                    student_serializer.is_valid(raise_exception=True)
                    student_serializer.save()
                except ValidationError as error:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'Invalid data',
                            'errors': error.detail
                        }
                    )
                except ValueError as error:
                    return Response(
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={
                            'status': 'error',
                            'message': str(error)
                        }
                    )

                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'Student updated',
                        'student': student_serializer.data
                    }
                )

            case 'DELETE':
                    user_token = request.query_params.get("token")
                    user_instance = User.objects.get(pk=user_token)
                    user_instance.delete()
                    return Response("Student Deleted")

            case _:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'status': 'fail',
                        'message': f'the method {request.method} is not allowed for this url'
                    }
                )

    # except Exception as ex:
    #     return Response(
    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         data={
    #             'status': 'fail',
    #             'message': 'a server error was thrown',
    #             'error': str(ex)
    #         }
    #     )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def topic(request):
    try:
        match request.method:
            case 'POST':
                new_topic = TopicSerializer(data=request.data)
                if new_topic.is_valid():
                    new_topic.save()
                    return Response(
                        status=status.HTTP_201_CREATED,
                        data={
                            "status": 'success',
                            'message': 'car has been created',
                            'topic': new_topic.data
                        }
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'the data provided is incorrect',
                            'error': new_topic.errors
                        }
                    )
            case 'GET':
                topic_id = request.query_params.get("id")
                if topic_id:
                    topic = Topic.objects.get(pk=topic_id)
                    topic_json = TopicSerializer(topic)
                else:
                    topics = Topic.objects.all()
                    topic_json = TopicSerializer(topics, many=True)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'retrieved all topics',
                        'topics': topic_json.data # convert to JSON compatible format
                    }
                )

            case 'PUT':
                try:
                    topic_id = request.query_params.get("id")
                    topic_instance = Topic.objects.get(pk=topic_id)
                    ts = TopicSerializer(instance=topic_instance, data=request.data, partial=True)
                    if ts.is_valid():
                        ts.save()
                        return Response("Topic updated")
                    else:
                        return Response({"Error": ts.errors}, status=500)
                except Exception as e:
                    return Response(f'Error: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            case 'DELETE':
                try:
                    topic_id = request.query_params.get("id")
                    topic_instance = Topic.objects.get(pk=topic_id)
                    topic_instance.delete()
                    return Response("Topic Deleted")
                except Exception as e:
                    return Response(f'Error: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            case _:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'status': 'fail',
                        'message': f'the method {request.method} is not allowed for this url'
                    }
                )

    except Exception as ex:
        print(ex)
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'status': 'fail',
                'message': 'a server error was thrown',
                'error': str(ex)
            }
        )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def feedback(request):
    try:
        match request.method:
            case 'POST':
                new_feedback = FeedbackSerializer(data=request.data)
                if new_feedback.is_valid():
                    new_feedback.save()
                    return Response(
                        status=status.HTTP_201_CREATED,
                        data={
                            "status": 'success',
                            'message': 'Feedback has been created',
                            'feedback': new_feedback.data
                        }
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'the data provided is incorrect',
                            'error': new_feedback.errors
                        }
                    )
            case 'GET':
                feedback_id = request.query_params.get("id")
                if feedback_id:
                    feedback = Feedback.objects.get(pk=feedback_id)
                    feedback_json = FeedbackSerializer(feedback)
                else:
                    feedback = Feedback.objects.all()
                    feedback_json = FeedbackSerializer(feedback, many=True)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'retrieved all feedbacks',
                        'feedback': feedback_json.data
                    }
                )

            case 'PUT':
                try:
                    feedback_id = request.query_params.get("id")
                    feedback_instance = Feedback.objects.get(pk=feedback_id)
                    fs = FeedbackSerializer(instance=feedback_instance, data=request.data, partial=True)
                    if fs.is_valid():
                        fs.save()
                        return Response(
                            status=status.HTTP_200_OK,
                            data={
                                'status': 'success',
                                'message': 'Feedback',
                                'feedback': fs.data
                            }
                        )
                    else:
                        return Response({"Error": fs.errors}, status=500)
                except Exception as e:
                    return Response(f'Error: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            case 'DELETE':
                try:
                    feedback_id = request.query_params.get("id")
                    feedback_instance = Feedback.objects.get(pk=feedback_id)
                    feedback_instance.delete()
                    return Response("Feedback Deleted")
                except Exception as e:
                    return Response(f'Error: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            case _:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'status': 'fail',
                        'message': f'the method {request.method} is not allowed for this url'
                    }
                )

    except Exception as ex:
        print(ex)
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'status': 'fail',
                'message': 'a server error was thrown',
                'error': str(ex)
            }
        )


class StudySessionSlotView(APIView):
    serializer_class = StudySessionSlotSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, pk):
        instance = StudySessionSlot.objects.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = StudySessionSlot.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk=None):
        if pk is not None:
            instance = StudySessionSlot.objects.get(pk=pk)
            mentor_hourly_rate = instance.mentor.teach_online
            response = self.serializer_class(instance).data
            response["hourly_rate"] = mentor_hourly_rate
            return Response(response)
        instances = StudySessionSlot.objects.all()
        response = []
        for instance in instances:
            slot_data = self.serializer_class(instance).data
            slot_data["hourly_rate"] = instance.mentor.teach_online
            response.append(slot_data)
        return Response(response, status=status.HTTP_200_OK)


class StudySessionView(APIView):
    serializer_class = StudySessionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, pk):
        instance = StudySession.objects.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = StudySession.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk=None):
        if pk is not None:
            instance = StudySession.objects.get(pk=pk)
            serializer = self.serializer_class(instance)
            return Response(serializer.data)
        instances = StudySession.objects.all()
        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data)

