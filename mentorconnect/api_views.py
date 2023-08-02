from .models import User, Student, Mentor, Topic, Feedback, StudySession, StudySessionSlot
from .forms import RegistrationForm, LoginForm
from .serializers import (MentorSerializer, StudentSerializer, TopicSerializer, FeedbackSerializer,
                          StudySessionSerializer, StudySessionSlotSerializer, StudentsFromChatsSerializer)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
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
from django.core.paginator import Paginator


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        userType = []
        try:
            user.mentor
            userType += ['mentor']
            token['mentor_id'] = user.mentor.id
        except Exception as error:
            print(error)

        try:
            user.student
            userType += ['student']
            token['student_id'] = user.student.id
        except Exception as error:
            print(error)

        
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


@api_view(['GET'])
def students_mentor_chats(request, user_id):
    user = User.objects.get(id=user_id)
    chats_serializer = StudentsFromChatsSerializer(user.mentor_chats, many=True)
    mentor_serializer = MentorSerializer(user.mentor)
    return Response(
            status=status.HTTP_200_OK,
            data={
                'status': 'success',
                'students': chats_serializer.data,
                'mentor': mentor_serializer.data
            }
        )

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
                user_id = request.query_params.get("id")
                topics_param = request.query_params.get("topics")
                cities_param = request.query_params.get("cities")
                page_number = request.query_params.get("page")

                mentors = Mentor.objects
                

                if user_token or topics_param or cities_param:
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

                    if user_token or user_id:
                        if user_token:
                            try:
                                decoded_token = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
                                mentor = User.objects.get(id=decoded_token['user_id']).mentor
                            except Exception as error:
                                
                                return Response(
                                    status=status.HTTP_400_BAD_REQUEST,
                                    data={
                                        'status': 'fail',
                                        'message': f'token not valid'
                                    }
                                )
                        elif user_id:
                            mentor.objects.get(id=user_id)

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
                    
                if page_number:
                    paginator = Paginator(mentors, 5)

                    try:
                        mentors = paginator.get_page(page_number)
                    except Exception as e:
                        
                        return Response(
                            status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'status': 'fail',
                                'message': 'Invalid page number'
                            }
                        )

                mentors_json = MentorSerializer(mentors, many=True)
                if page_number:
                    data = {
                        'status': 'success',
                        'message': 'retrieved mentors',
                        'mentors': mentors_json.data,
                        'num_pages': mentors.paginator.num_pages,
                        'current_page': mentors.number,
                        'has_previous': mentors.has_previous(),
                        'has_next': mentors.has_next(),
                    }
                else:
                    data = {
                        'status': 'success',
                        'message': 'retrieved mentors',
                        'mentors': mentors_json.data,
                    }

                return Response(
                    status=status.HTTP_200_OK,
                    data=data
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
                        
                    except Exception as error:
                        
                        return Response(
                            status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'status': 'fail',
                                'message': f'token not valid'
                            }
                        )
                    student_serializer = StudentSerializer(student)  # Serialize the Student instance
                    
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
                        
                    except Exception as error:
                        
                        return Response(
                            status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'status': 'fail',
                                'message': f'token not valid'
                            }
                        )
                    student_serializer = StudentSerializer(student)  # Serialize the Student instance
                    
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
        
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'status': 'fail',
                'message': 'a server error was thrown',
                'error': str(ex)
            }
        )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def study_session_slot_view(request, pk=None):
    try:
        match request.method:
            case 'POST':
                new_slot = StudySessionSlotSerializer(data=request.data)
                if new_slot.is_valid():
                    new_slot.save()
                    return Response(
                        status=status.HTTP_201_CREATED,
                        data={
                            "status": 'success',
                            'message': 'Study Session Slot has been created',
                            'slot': new_slot.data
                        }
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'the data provided is incorrect',
                            'error': new_slot.errors
                        }
                    )
            case 'PUT':
                slot_id = pk
                slot_instance = StudySessionSlot.objects.get(pk=slot_id)
                slot_serializer = StudySessionSlotSerializer(
                    instance=slot_instance, data=request.data, partial=True)
                if slot_serializer.is_valid():
                    slot_serializer.save()
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            'status': 'success',
                            'message': 'Study Session Slot has been updated',
                            'slot': slot_serializer.data
                        }
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'the data provided is incorrect',
                            'error': slot_serializer.errors
                        }
                    )
            case 'DELETE':
                try:
                    slot_id = pk
                    slot_instance = StudySessionSlot.objects.get(pk=slot_id)
                    slot_instance.delete()
                    return Response("Study Session Slot Deleted")
                except Exception as e:
                    return Response(f'Error: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            case 'GET':
                try:
                    slot_id = pk
                    if slot_id is not None:
                        slot_instance = StudySessionSlot.objects.get(pk=slot_id)
                        # mentor_hourly_rate = slot_instance.mentor.slot.rate
                        response = StudySessionSlotSerializer(slot_instance).data
                        # response["hourly_rate"] = mentor_hourly_rate
                        return Response(response)
                    slots = StudySessionSlot.objects.all()
                    response = StudySessionSlotSerializer(slots, many=True).data
                    return Response(response, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(f'Error: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as ex:
        
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'status': 'fail',
                'message': 'a server error was thrown',
                'error': str(ex)
            }
        )

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def study_session_view(request, pk=None):
    try:
        match request.method:
            case 'POST':
                new_session = StudySessionSerializer(data=request.data)
                if new_session.is_valid():
                    new_session.save()
                    return Response(
                        status=status.HTTP_201_CREATED,
                        data={
                            "status": 'success',
                            'message': 'Study Session has been created',
                            'session': new_session.data
                        }
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'the data provided is incorrect',
                            'error': new_session.errors
                        }
                    )
            case 'PUT':
                session_id = pk
                
                session_instance = StudySession.objects.get(pk=session_id)
                session_serializer = StudySessionSerializer(
                    instance=session_instance, data=request.data, partial=True)
                if session_serializer.is_valid():
                    session_serializer.save()
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            'status': 'success',
                            'message': 'Study Session has been updated',
                            'session': session_serializer.data
                        }
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'the data provided is incorrect',
                            'error': session_serializer.errors
                        }
                    )
            case 'DELETE':
                try:
                    session_id = pk
                    session_instance = StudySession.objects.get(pk=session_id)
                    session_instance.delete()
                    return Response("Study Session Deleted")
                except Exception as e:
                    return Response(f'Error: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            case 'GET':
                try:
                    mentor_id = request.query_params.get("mentor_id")

                    session_id = pk

                    if mentor_id:
                        print(mentor_id)
                        session_instance = StudySession.objects.filter(slot__mentor_id=mentor_id)
                        print("🚀 ~ file: api_views.py:815 ~ session_instance:", session_instance)
                        session_serializer = StudySessionSerializer(session_instance, many=True)
                        return Response(data=session_serializer.data)

                    elif session_id:
                        session_instance = StudySession.objects.get(pk=session_id)
                        return Response(StudySessionSerializer(session_instance).data)
                    sessions = StudySession.objects.all()
                    serializer = StudySessionSerializer(sessions, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(f'Error: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    except Exception as ex:
        
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'status': 'fail',
                'message': 'a server error was thrown',
                'error': str(ex)
            }
        )
# Function to receive user_id ad the associated student and returns all the study sessions associated with the student,
# and that StudySession.student_approved = False
def get_student_study_sessions(user_id):
    try:
        student = Student.objects.get(user_id=user_id)
        sessions = StudySession.objects.filter(student=student, student_approved=False)
        serializer = StudySessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return None
