import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Achievements, Colors
from sessions_rounds.models import Pods
from .serializers import AchievementsSerializer, ColorsSerializer

from achievements.helpers import AchievementCleaverService, make_achievement_map


@api_view(["GET"])
def get_achievements_with_restrictions(request):
    achievements = Achievements.objects.filter(deleted=False).prefetch_related(
        "restrictions"
    )
    serializer = AchievementsSerializer(achievements, many=True).data
    map = make_achievement_map(serializer)
    return Response({"map": map, "data": serializer}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_colors(request):
    colors_objects = Colors.objects.all()
    colors = [
        {"id": c["id"], "name": c["name"].title()}
        for c in ColorsSerializer(colors_objects, many=True).data
    ]

    return Response(colors, status=status.HTTP_200_OK)


@api_view(["POST"])
def upsert_achievements(request):
    body = json.loads(request.body.decode("utf-8"))
    id = body.get("id", None)
    deleted = body.get("deleted", None)
    point_value = body.get("point_value", None)
    parent_id = body.get("parent_id", None)
    name = body.get("name", None)

    if id is None and (point_value is None or name is None):
        return Response(
            {
                "message": "Information to create/update achievement missing from request body."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    achievement, _ = Achievements.objects.update_or_create(
        id=(id if id else None),
        defaults={
            "name": name or None,
            "deleted": deleted or False,
            "point_value": point_value or None,
            "parent_id": parent_id,
        },
    )
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
    pod_id = body.get("pod", None)
    winner_info = body.get("winnerInfo", None)

    if not round_id or not session_id or not pod_id or not winner_info:
        return Response(
            {"message": "Missing round and/or session information"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    achievement_service = AchievementCleaverService(
        participants=participants,
        round=round_id,
        session=session_id,
        pod_id=pod_id,
        winner_info=winner_info,
    )
    achievement_service.build_service()
    Pods.objects.filter(id=pod_id).update(submitted=True)
    return Response(status=status.HTTP_201_CREATED)
