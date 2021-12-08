from os import name
from typing import List
from django import forms
from django.core.checks import messages
from ninja import NinjaAPI
from .models import UserChatt
from .schema import *
from ninja.errors import HttpError
from django.db.models import Q
from django.db import transaction
ApiUser = NinjaAPI()


@ApiUser.get('/all', response=List[UserSchema])
def GetAllUser(request):
    users = UserChatt.objects.filter(is_active=True)
    return list(users)


@ApiUser.post('/create', response=UserSchema)
def CreateUser(request, payload: UserSchema):
    # Create User by username
    user = UserChatt.objects.filter(username=payload.username)
    if user:
        raise HttpError(500, 'Username is taken')
    else:
        user = UserChatt.objects.create(**payload.dict())
        return user


# create message step by step
# 1. create rooms
# 2. add participants
# 3. send message
@ApiUser.post('/{username}/messages/to/personal')
def SendMessage(request, username, payload: MessageSchema):
    if username == payload.receiver:
        raise HttpError(500, 'You cant sent message to your self')
    # cek if the receiver is exist
    sender = UserChatt.objects.get(username=username)
    receiver = UserChatt.objects.get(username=payload.receiver)
    if not receiver or not sender:
        raise HttpError(404, 'The receiver or sender is not found')
    # check rooms
    rooms_name_v1 = username + "_" + payload.receiver
    rooms_name_v2 = payload.receiver + "_" + username
    with transaction.atomic():
      rooms = Rooms.objects.filter(Q(name=rooms_name_v1) | Q(name=rooms_name_v2)).first()
      # if rooms does not exist[they never talk before]
      if not rooms:
          rooms = Rooms.objects.create(name=rooms_name_v1)
          print("rooms => ", rooms.id)
          participat_dict = [
              Participants(rooms_id=rooms,
                            participant=sender),  #sender
              Participants(rooms_id=rooms,
                            participant=receiver),  #receiver
          ]
          ps = Participants.objects.bulk_create(participat_dict)
      # send the chatt
      print("rooms final => ", rooms.id)
      chatt = Chatt()
      print("sender =>", sender.username)
      chatt.participant = Participants.objects.filter(Q(participant=sender) & Q(rooms_id=rooms)).first()
      chatt.message = payload.message
      chatt.rooms = rooms
      chatt.read_by = ""
      chatt.save()
      return {
        "chatt": {
          "id": chatt.pk,
          "sender": chatt.participant.participant.username,
          "message": chatt.message,
          "rooms": chatt.rooms.pk,
          "rooms_name":chatt.rooms.name,
        }
      }


@ApiUser.get('/{username}/messages/unread')
def GetUnreadMessage(request, username):
  # get all message for user
  user = UserChatt.objects.filter(username=username).first()
  print(" User =>",user.pk)
  if not user:
    raise HttpError(404, "Username is not found")
  # mapListOfMessage = {
  #   'read_by': 'read_by',
  #   'rooms_id': 'rooms_id',
  #   'message': 'message',
  #   'part_id': 'part_id'
  # }
  listOfMessage = Participants.objects.raw(
    "SELECT c.read_by, c.rooms_id, c.message, p.id part_id  FROM chatt_participants p JOIN chatt_chatt c ON p.id = c.participant_id" +
    "WHERE p.participant_id = %s ", [user.id]
  )
  for m in listOfMessage:
    print(m.read_by)

  return {}
