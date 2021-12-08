from typing import List
from django.core.checks import messages
from ninja import ModelSchema, schema
from .models import *
from ninja.orm import create_schema
# Exception class


class UserSchema(ModelSchema):
    class Config:
        model = UserChatt
        model_exclude = ['id']
        # model_fields = ['username', 'is_active']


unread_message_schema = create_schema(Participants, depth=1, fields=['id', 'participant', 'rooms_id'])

class ParticipantSchema(ModelSchema):
    class Config:
        model = Participants
        model_fields = ['id','participant', 'rooms_id']


class MessageSchema(schema.Schema):
    receiver: str
    message: str

class UnreadMessage(schema.Schema):
    room_id: int
    messages: List[MessageSchema]

    