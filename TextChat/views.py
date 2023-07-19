from django.shortcuts import render
from django.http import HttpResponse
from .models import Chat, Message
# Create your views here.


def chatHome(request):
    messages = Message.objects.filter(chat_id='test')
    print(messages)
    return HttpResponse('hello from chat')

