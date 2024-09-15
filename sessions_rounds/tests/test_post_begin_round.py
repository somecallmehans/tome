import pytest
import random
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock

from achievements.models import Achievements
from sessions_rounds.models import Sessions, Rounds
from sessions_rounds.serializers import RoundsSerializer, SessionSerializer
from sessions_rounds.helpers import generate_pods
from users.models import Participants, ParticipantAchievements

test_participants = [
    {"id": 1, "name": "Glennis Sansam"},
    {"id": 2, "name": "Sara Dewhurst"},
    {"id": 3, "name": "Uriel Cohani"},
    {"id": 4, "name": "Noella Gannon"},
    {"id": 5, "name": "Teriann Pendergast"},
    {"id": 6, "name": "Ezra Vasyutochkin"},
    {"id": 7, "name": "Janna Erskine Sandys"},
    {"id": 8, "name": "Gibby Abrahart"},
]

test_participants_no_id = [
    {"name": "Celestia Clearie"},
    {"name": "Gilbert Loxton"},
    {"name": "Sammie Cruikshanks"},
]

combined_list = test_participants + test_participants_no_id


@pytest.mark.django_db
@mock.patch("users.models.datetime", side_effect=lambda *args, **kw: date(*args, **kw))
def test_post_begin_round(mock_date):
    """Begin a new round where everyone gets participation points."""
    client = APIClient()
    url = reverse("begin_round")

    mocked_today = datetime(2024, 11, 25)
    mock_date.today.return_value = mocked_today
    mocked_mmyy = mocked_today.strftime("%m-%y")

    s1 = Sessions.objects.create(id=1, month_year=mocked_mmyy, closed=True)
    r1 = Rounds.objects.create(id=1, session_id=s1, round_number=1)
    a1 = Achievements.objects.create(
        id=24, name="Participation Trophy", point_value=3, parent_id=None
    )

    session_serializer = SessionSerializer(s1)
    round_serializer = RoundsSerializer(r1)

    # Add some of the participants to the testdb
    for p in test_participants:
        Participants.objects.create(name=p["name"])

    payload = {
        "round": round_serializer.data["id"],
        "session": session_serializer.data["id"],
        "participants": combined_list,
    }

    response = client.post(url, payload, format="json")
    parsed_res = response.json()
    breakpoint()


def pod_factory(pods):
    four_pods = 0
    three_pods = 0

    generated_pods = generate_pods(pods)

    for s in generated_pods:
        if len(s) == 4:
            four_pods += 1
        else:
            three_pods += 1

    return four_pods, three_pods


def test_post_pod_generator():
    """Test that the pod generator correctly makes pods of
    4 and 3 based on the number of participants it receives."""

    # 17 Players
    four_pods, three_pods = pod_factory(pods=list(range(1, 18)))
    assert four_pods == 2
    assert three_pods == 3

    # 16 Players
    four_pods, three_pods = pod_factory(pods=list(range(1, 17)))
    assert four_pods == 4
    assert three_pods == 0

    # 27 Players
    four_pods, three_pods = pod_factory(pods=list(range(1, 28)))
    assert four_pods == 6
    assert three_pods == 1

    # 33 Players
    four_pods, three_pods = pod_factory(pods=list(range(1, 30)))
    assert four_pods == 5
    assert three_pods == 3
