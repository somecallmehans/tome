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
def post_participant(request):
    body = json.loads(request.body.decode("utf-8"))
    p_name = body.get("name", None)

    try:
        new_participant = Participants.objects.create(name=p_name)
        serializer = ParticipantsSerializer(new_participant)
    except IntegrityError:
        return Response(
            {"message": "Name not provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    return Response(serializer.data, status=status.HTTP_201_CREATED)


