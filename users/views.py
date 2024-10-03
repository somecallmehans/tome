import json

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Participants
from .serializers import ParticipantsSerializer


@api_view(["GET"])
def get_all_participants(request):
    participants = Participants.objects.all().filter(deleted=False)
    serializer = ParticipantsSerializer(participants, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def upsert_participant(request):
    body = json.loads(request.body.decode("utf-8"))
    id = body.get("id", None)
    name = body.get("name", None)
    deleted = body.get("deleted", None)

    if not id and not name:
        return Response(
            {"message": "Name not provided for new participant"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    participant, _ = Participants.objects.update_or_create(
        id=(id if id else None),
        defaults={"name": name, "deleted": deleted or False},
    )
    serializer = ParticipantsSerializer(participant)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


class Login(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)
