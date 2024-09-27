import pytest
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock

from users.models import Participants
from users.serializers import ParticipantsSerializer

from achievements.models import Achievements
from sessions_rounds.models import Sessions, Rounds
from sessions_rounds.serializers import RoundsSerializer, SessionSerializer
from sessions_rounds.helpers import generate_pods

test_participants_no_id = [
    {"name": "Celestia Clearie"},
    {"name": "Gilbert Loxton"},
    {"name": "Sammie Cruikshanks"},
]


@pytest.mark.django_db(serialized_rollback=True)
@mock.patch("users.models.datetime", side_effect=lambda *args, **kw: date(*args, **kw))
def test_post_begin_round(
    mock_date, create_base_participants, create_base_session_and_rounds
):
    """Begin a new round where everyone gets participation points."""
    client = APIClient()
    url = reverse("begin_round")

    mocked_today = datetime(2024, 11, 25)
    mock_date.today.return_value = mocked_today

    session = Sessions.objects.get(id=11)
    round = Rounds.objects.get(id=11)
    Achievements.objects.create(
        id=24, name="Participation Trophy", point_value=3, parent_id=None
    )

    session_serializer = SessionSerializer(session)
    round_serializer = RoundsSerializer(round)

    p_data = Participants.objects.all()
    p_serialized = ParticipantsSerializer(p_data, many=True)
    p_to_send = [{"id": p["id"], "name": p["name"]} for p in p_serialized.data]
    payload = {
        "round": round_serializer.data["id"],
        "session": session_serializer.data["id"],
        "participants": p_to_send + test_participants_no_id,
    }

    response = client.post(url, payload, format="json")

    parsed_res = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert len(parsed_res[0]) == 4
    assert len(parsed_res[1]) == 3


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

    # 6 Players
    four_pods, three_pods = pod_factory(pods=list(range(1, 7)))
    assert four_pods == 0
    assert three_pods == 2

    # 16 Players
    four_pods, three_pods = pod_factory(pods=list(range(1, 17)))
    assert four_pods == 4
    assert three_pods == 0

    # 17 Players
    four_pods, three_pods = pod_factory(pods=list(range(1, 18)))
    assert four_pods == 2
    assert three_pods == 3

    # 27 Players
    four_pods, three_pods = pod_factory(pods=list(range(1, 28)))
    assert four_pods == 6
    assert three_pods == 1

    # 33 Players
    four_pods, three_pods = pod_factory(pods=list(range(1, 34)))
    assert four_pods == 6
    assert three_pods == 3
