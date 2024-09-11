import json

from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Sessions, Rounds
from .serializers import SessionSerializer
from users.models import Participants

POST = "POST"


@api_view(["GET", "POST"])
def sessions_and_rounds(request):
    """Get or create a sessions/rounds for today."""
    if request.method == POST:
        body = json.loads(request.body.decode("utf-8"))
        today = datetime.today()
        mm_yy = today.strftime("%m-%y")
        new_session = Sessions.objects.create(month_year=mm_yy)
        Rounds.objects.create(session_id=new_session, round_number=1)
        Rounds.objects.create(session_id=new_session, round_number=2)
        serializer = SessionSerializer(new_session)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    session_id = body.get("session_id", None)

    participant_ids = body.get("participants", [])
    existing_ids = Participants.objects.filter(pk__in=participant_ids).values_list(
        "id", flat=True
    )
    new_ids = [x for x in participant_ids if x not in existing_ids]

    # this needs to be dicts of id + name which means the
    # req body also needs to include this info
    for id in new_ids:
        Participants.objects.create(id=id, name={})

    return Response()
