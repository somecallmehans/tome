from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Sessions, Rounds
from .serializers import SessionSerializer


POST = "POST"


@api_view(["GET", "POST"])
def sessions_and_rounds(request):
    """Get or create a sessions/rounds for today."""
    today = datetime.today()
    mm_yy = today.strftime("%m-%y")

    if request.method == POST:
        new_session = Sessions.objects.create(month_year=mm_yy)
        Rounds.objects.create(session_id=new_session, round_number=1)
        Rounds.objects.create(session_id=new_session, round_number=2)
        serializer = SessionSerializer(new_session)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    try:
        current_session = Sessions.objects.get(month_year=mm_yy, closed=False)
        serializer = SessionSerializer(current_session)
    except Sessions.DoesNotExist:
        return Response(
            {"message": "Open session for current month not found."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(serializer.data, status=status.HTTP_200_OK)
