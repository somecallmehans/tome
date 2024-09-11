import pytest
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock


@pytest.mark.django_db
@mock.patch(
    "sessions_rounds.views.datetime", side_effect=lambda *args, **kw: date(*args, **kw)
)
def test_post_new_session_no_id(mock_date):
    client = APIClient()

    url = reverse("make_sessions_and_rounds")

    mocked_today = datetime(2024, 11, 25)
    mock_date.today.return_value = mocked_today

    payload = {}

    response = client.post(url, payload, format="json")
    parsed_res = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert parsed_res["id"] == 1 and parsed_res["month_year"] == "11-24"
    assert len(parsed_res["rounds"]) == 2


# @pytest.mark.django_db
# def test_post_new_session_no_id():
#     client = APIClient()
# for n in range(1, 20):
#     Participants.objects.create(id=n, name=f"GUY-{n}")

#     url = reverse('make_sessions_and_rounds')

#     payload = {"session_id": 111}

#     response = client.post(url, payload, format='json')

#     assert response.status_code == status.HTTP_200_OK
