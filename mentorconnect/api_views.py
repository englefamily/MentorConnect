from .serializers import MentorSerializer, StudentSerializer, TopicSerializer, SubTopicSerializer, FeedbackSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Student, Mentor, Topic, SubTopic, Feedback
from rest_framework.views import APIView
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.views.decorators.cache import cache_page
from django.core.cache import cache


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
                user_token = request.query_params.get("token")
                if not user_token:
                    mentors = Mentor.objects.all()
                    mentors_json = MentorSerializer(mentors, many=True)
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            'status': 'success',
                            'message': 'retrieved all mentors',
                            'mentors': mentors_json.data  # convert to JSON compatible format
                        }
                    )
                    # return Response(
                    #     status=status.HTTP_400_BAD_REQUEST,
                    #     data={
                    #         'status': 'fail',
                    #         'message': f'token not found'
                    #     }
                    # )
                try:
                    mentor = Token.objects.get(key=user_token).mentor
                except Exception as error:
                    if str(error) == 'Token matching query does not exist.':
                        return Response(
                            status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'status': 'fail',
                                'message': f'token not exist'
                            }
                        )

                mentor_json = MentorSerializer(mentor)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'user found',
                        'mentor': mentor_json.data # convert to JSON compatible format
                    }
                )

            case 'PUT':
                    user_token = request.query_params.get("token")
                    mentor_instance = Token.objects.get(key=user_token).user.mentor
                    mentor_data = request.data
                    user = mentor_data.pop('user', None)
                    ms = MentorSerializer(instance=mentor_instance, data=mentor_data, context={'user': user}, partial=True)
                    if ms.is_valid():
                        try:
                            ms.save()
                        except ValueError as error:
                            return Response({"Error": error}, status=500)
                        return Response(
                            status=status.HTTP_200_OK,
                            data={
                                'status': 'success',
                                'message': 'Mentor updated',
                                'mentor': ms.data  # convert to JSON compatible format
                            }
                        )
                    else:
                        return Response({"Error": ms.errors}, status=500)

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
        # print(ex)
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'status': 'fail',
                'message': 'a server error was thrown',
                'error': str(ex) # convert to string to make it JSON serializable
            }
        )

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def student(request):
    try:
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
                            'message': 'Mentor profile created',
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
                if not user_token:
                    students = Student.objects.all()
                    students_json = StudentSerializer(students, many=True)
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            'status': 'success',
                            'message': 'retrieved all students',
                            'students': students_json.data  # convert to JSON compatible format
                        }
                    )
                try:
                    student = Token.objects.get(key=user_token).student
                except Exception as error: #todo fix Exception
                    if str(error) == 'Token matching query does not exist.':
                        return Response(
                            status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'status': 'fail',
                                'message': f'token not exist'
                            }
                        )

                student_json = StudentSerializer(student)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'student found',
                        'student': student_json.data # convert to JSON compatible format
                    }
                )

            case 'PUT':
                user_token = request.query_params.get("token")
                student_instance = Token.objects.get(key=user_token).user.student
                student_data = request.data
                user = student_data.pop('user', None)
                ss = StudentSerializer(instance=student_instance, data=student_data, context={'user': user},partial=True)
                if ss.is_valid():
                    try:
                        ss.save()
                    except ValueError as error:
                        return Response({"Error": error}, status=500)
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            'status': 'success',
                            'message': 'Student updated',
                            'student': ss.data
                        }
                    )
                else:
                    return Response({"Error": ss.errors}, status=500)


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

    except Exception as ex:
        # print(ex)
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'status': 'fail',
                'message': 'a server error was thrown',
                'error': str(ex)
            }
        )


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
def sub_topic(request):
    try:
        match request.method:
            case 'POST':
                new_sub_topic = SubTopicSerializer(data=request.data)
                if new_sub_topic.is_valid():
                    new_sub_topic.save()
                    return Response(
                        status=status.HTTP_201_CREATED,
                        data={
                            "status": 'success',
                            'message': 'Sub topic has been created',
                            'sub _topic': new_sub_topic.data
                        }
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'the data provided is incorrect',
                            'error': new_sub_topic.errors
                        }
                    )
            case 'GET':
                sub_topic_id = request.query_params.get("id")
                if sub_topic_id:
                    sub_topic = SubTopic.objects.get(pk=sub_topic_id)
                    sub_topic_json = SubTopicSerializer(sub_topic)
                else:
                    sub_topics = SubTopic.objects.all()
                    sub_topic_json = SubTopicSerializer(sub_topics, many=True)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'retrieved all topics',
                        'sub_topic': sub_topic_json.data
                    }
                )

            case 'PUT':
                try:
                    sub_topic_id = request.query_params.get("id")
                    sub_topic_instance = SubTopic.objects.get(pk=sub_topic_id)
                    sts = SubTopicSerializer(instance=sub_topic_instance, data=request.data, partial=True)
                    if sts.is_valid():
                        sts.save()
                        return Response("Sub topic updated")
                    else:
                        return Response({"Error": sts.errors}, status=500)
                except Exception as e:
                    return Response(f'Error: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            case 'DELETE':
                try:
                    sub_topic_id = request.query_params.get("id")
                    sub_topic_instance = SubTopic.objects.get(pk=sub_topic_id)
                    sub_topic_instance.delete()
                    return Response("Sub topic Deleted")
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
