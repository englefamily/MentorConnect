from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return HttpResponse("Welcome to MentorConnect! from hananel")


@csrf_exempt
def bye(request):
    return HttpResponse("Bye Bye from MentorConnect! Come back soon!")