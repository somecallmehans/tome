import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Achievements
from .serializers import AchievementsSerializer

from achievements.helpers import AchievementCleaverService


@api_view(["GET"])
def get_achievements_with_restrictions(request):
    achievements = Achievements.objects.prefetch_related("restrictions")
    serializer = AchievementsSerializer(achievements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def upsert_achievements(request):
    body = json.loads(request.body.decode("utf-8"))
    id = body.get("id", None)
    point_value = body.get("point_value", None)
    name = body.get("name", None)

    if id is None and (point_value is None or name is None):
        return Response(
            {
                "message": "Information to create/update achievement missing from request body."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    achievement, _ = Achievements.objects.update_or_create(**body)
    serialized = AchievementsSerializer(achievement)

    return Response(serialized.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def post_achievements_for_participants(request):
    """
    Take in session_id, round_id, and a list of participants,
    each with a list of achievements earned
    that round and log them each as new records under the ParticipantsAchievements table.
    """
    # TODO First iteration of this endpoint will not consider restrictions on achievements
    # as that functionality will likely require it's own service to handle.
    body = json.loads(request.body.decode("utf-8"))
    participants = body.get("participants", None)
    round_id = body.get("round", None)
    session_id = body.get("session", None)

    if not round_id or not session_id:
        return Response(
            {"message": "Missing round and/or session information"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    achievement_service = AchievementCleaverService(
        participants=participants, round=round_id, session=session_id
    )
    achievement_service.build_service()
    return Response(status=status.HTTP_201_CREATED)
