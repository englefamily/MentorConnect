from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def lobby(request):
    return render(request, 'videochat/lobby.html')


def room(request):
    return render(request, 'videochat/room.html')


# TODO: Move appID, appCertificate to `EviromentVariables` for Deployment
def getToken(request):
    appId = "de3b68dea39d4e2ea71981a4e5277def"
    appCertificate = "b059577cccdb41a69817e2bdf98112c2"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name': data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name': member.name}, safe=False)


# @csrf_exempt
# def deleteMember(request):
#     data = json.loads(request.body)
#     member = RoomMember.objects.get(
#         name=data['name'],
#         uid=data['UID'],
#         room_name=data['room_name']
#     )
#     member.delete()
#     return JsonResponse('Member deleted', safe=False)


@csrf_exempt
def deleteMember(request):
    try:
        member = RoomMember.objects.get(
            Q(name=request.POST['name']) & Q(room_name=request.POST['room_name']) & Q(UID=request.POST['UID'])
        )
        member.delete()
        print('Deleted member:')
        print(member)
        return JsonResponse({'member_exists': True,'member_deleted': True}, safe=False)

    except RoomMember.DoesNotExist: 
        # handle the case when RoomMember does not exist
        print('RoomMember Does not exist. Not able to delete.')
        return JsonResponse({'member_exists': False,'member_deleted': False}, safe=False)