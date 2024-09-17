import pytest
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock

from achievements.models import Achievements
from sessions_rounds.models import Sessions, Rounds
from sessions_rounds.serializers import RoundsSerializer, SessionSerializer
from sessions_rounds.test_helpers import participant_achievement_factory, combined_list
from users.models import Participants


@pytest.mark.django_db(serialized_rollback=True)
@mock.patch("users.models.datetime", side_effect=lambda *args, **kw: date(*args, **kw))
def test_post_begin_round_two_session_two(
    mock_date, create_base_participants, create_base_session_and_rounds
):
    """Begin a new round that is 'mid season'.

    Some players will have some existing achievements and get
    sorted into most -> least points based pods."""

    client = APIClient()
    url = reverse("begin_round")

    mocked_today = datetime(2024, 11, 25)
    mock_date.today.return_value = mocked_today

    # One real achievement and some fake ones
    participation_award = Achievements.objects.create(
        id=24, name="Participation Trophy", point_value=3, parent_id=None
    )
    win_1 = Achievements.objects.create(
        id=1, name="Regular Win", point_value=1, parent_id=None
    )
    win_2 = Achievements.objects.create(
        id=2, name="Mega Win", point_value=3, parent_id=None
    )

    sessions = Sessions.objects.all()
    rounds = Rounds.objects.all()

    session_serializer = SessionSerializer(sessions[1])
    round_serializer = RoundsSerializer(rounds[3])

    participant_data = Participants.objects.all()

    ## P1 Achievements. Earned participation in S1 R1 AND S2 R1
    participant_achievement_factory(
        session=sessions[0],
        round=rounds[0],
        participant=participant_data[0],
        achievement=participation_award,
    )
    participant_achievement_factory(
        session=sessions[0],
        round=rounds[0],
        participant=participant_data[0],
        achievement=win_1,
    )
    participant_achievement_factory(
        session=sessions[1],
        round=rounds[2],
        participant=participant_data[0],
        achievement=participation_award,
    )

    ## P2 Achievements. Earned participation in S1 R1 AND S2 R1
    participant_achievement_factory(
        session=sessions[0],
        round=rounds[0],
        participant=participant_data[1],
        achievement=participation_award,
    )
    participant_achievement_factory(
        session=sessions[1],
        round=rounds[2],
        participant=participant_data[1],
        achievement=participation_award,
    )

    ## P3 Achievements (NO S2 Participation)
    participant_achievement_factory(
        session=sessions[0],
        round=rounds[0],
        participant=participant_data[2],
        achievement=participation_award,
    )
    participant_achievement_factory(
        session=sessions[0],
        round=rounds[1],
        participant=participant_data[2],
        achievement=win_2,
    )

    ## P4 Achievements (NO S2 Participation)
    participant_achievement_factory(
        session=sessions[0],
        round=rounds[0],
        participant=participant_data[3],
        achievement=participation_award,
    )

    payload = {
        "round": round_serializer.data["id"],
        "session": session_serializer.data["id"],
        "participants": combined_list,
    }

    response = client.post(url, payload, format="json")
    parsed_res = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert parsed_res[0] == [
        {"id": 3, "name": "Uriel Cohani", "total_points_current_month": 9},
        {"id": 1, "name": "Glennis Sansam", "total_points_current_month": 7},
        {"id": 2, "name": "Sara Dewhurst", "total_points_current_month": 6},
        {"id": 4, "name": "Noella Gannon", "total_points_current_month": 6},
    ]
    assert parsed_res[1] == [
        {"id": 5, "name": "Celestia Clearie", "total_points_current_month": 3},
        {"id": 6, "name": "Gilbert Loxton", "total_points_current_month": 3},
        {"id": 7, "name": "Sammie Cruikshanks", "total_points_current_month": 3},
    ]
