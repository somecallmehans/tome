import json

from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Participants
from .serializers import ParticipantsSerializer


@api_view(["GET"])
def get_all_participants():
    participants = Participants.objects.all().filter(deleted=False)
    serializer = ParticipantsSerializer(participants, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def upsert_participant(request):
    body = json.loads(request.body.decode("utf-8"))
    id = body.get("id", None)
    name = body.get("name", None)

    if not id and not name:
        return Response(
            {"message": "Name not provided for new participant"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    participant, _ = Participants.objects.update_or_create(**body)
    serializer = ParticipantsSerializer(participant)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
