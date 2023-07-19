from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from django.db.models import Q


@api_view(['GET'])
def get_messages(request):
    # try:
    if True:
        chat_id = request.query_params.get("id")
        chats = Chat.objects.filter(
            Q(id__contains=f'{chat_id}-') | Q(id__contains=f'-{chat_id}')
        )
        # get users ids



    # except Exception as ex:
    # print(ex)
    # return Response(
    #     status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     data={
    #         'status': 'fail',
    #         'message': 'a server error was thrown',
    #         'error': str(ex)
    #     }
    # )

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def chat(request):
    print(request.data)
    # try:
    if True:
        match request.method:
            case 'POST':
                print(request.data)
                chat_serializer = ChatSerializer(data=request.data)
                if chat_serializer.is_valid():
                    chat_serializer.save()
                    return Response(
                        status=status.HTTP_201_CREATED,
                        data={
                            "status": 'success',
                            'message': 'chat has been created',
                            'chat': chat_serializer.data
                        }
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'message': 'the data provided is incorrect',
                            'error': chat_serializer.errors
                        }
                    )
            case 'GET':
                chat_id = request.query_params.get("id")
                if chat_id:
                    chats = Chat.objects.filter(
                        Q(id__contains=f'{chat_id}-') | Q(id__contains=f'-{chat_id}')
                    )
                    chat_serializer = ChatSerializer(chats, many=True)
                else:
                    chats = Chat.objects.all()
                    chat_serializer = ChatSerializer(chats, many=True)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'message': 'retrieved all chats',
                        'chats': chat_serializer.data # convert to JSON compatible format
                    }
                )


            case 'DELETE':
                try:
                    chat_id = request.query_params.get("id")
                    chat_instance = Chat.objects.get(pk=chat_id)
                    chat_instance.delete()
                    return Response("Chat Deleted")
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

    # except Exception as ex:
    #     print(ex)
    #     return Response(
    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         data={
    #             'status': 'fail',
    #             'message': 'a server error was thrown',
    #             'error': str(ex)
    #         }
    #     )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def message(request):
    try:
        match request.method:
            case 'POST':
                message_serializer = MessageSerializer(data=request.data)
                if message_serializer.is_valid():
                    message_serializer.save()
                    return Response(
                        status=status.HTTP_201_CREATED,
                        data={
                            "status": 'success',
                            'message': message_serializer.data
                        }
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'fail',
                            'error': message_serializer.errors
                        }
                    )
            case 'GET':
                message_id = request.query_params.get("id")
                if message_id:
                    message = Message.objects.get(pk=message_id)
                    message_serializer = MessageSerializer(message)
                else:
                    messages = Message.objects.all()
                    message_serializer = MessageSerializer(messages, many=True)
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status': 'success',
                        'messages': message_serializer.data  # convert to JSON compatible format
                    }
                )

            case 'DELETE':
                try:
                    message_id = request.query_params.get("id")
                    message_instance = Message.objects.get(pk=message_id)
                    message_instance.delete()
                    return Response("Message Deleted")
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
