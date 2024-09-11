import pytest
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock

from sessions_rounds.models import Sessions, Rounds


@pytest.mark.django_db
@mock.patch(
    "sessions_rounds.views.datetime", side_effect=lambda *args, **kw: date(*args, **kw)
)
def test_get_current_session_and_rounds(mock_date):
    client = APIClient()

    url = reverse("make_sessions_and_rounds")

    mocked_today = datetime(2024, 11, 25)
    mock_date.today.return_value = mocked_today
    mocked_mmyy = mocked_today.strftime("%m-%y")

    s1 = Sessions.objects.create(id=1, month_year=mocked_mmyy, closed=True)
    s2 = Sessions.objects.create(id=2, month_year=mocked_mmyy, closed=False)
    Rounds.objects.create(id=1, session_id=s1, round_number=1)
    Rounds.objects.create(id=2, session_id=s1, round_number=2)
    Rounds.objects.create(id=3, session_id=s2, round_number=1)
    Rounds.objects.create(id=4, session_id=s2, round_number=2)

    res = client.get(url)
    parsed_res = res.json()

    assert res.status_code == status.HTTP_200_OK
    assert parsed_res["id"] == 2
    assert parsed_res["rounds"][0]["id"] == 3
    assert parsed_res["rounds"][1]["id"] == 4


@pytest.mark.django_db
def test_get_no_session():
    client = APIClient()

    url = reverse("make_sessions_and_rounds")

    res = client.get(url)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
