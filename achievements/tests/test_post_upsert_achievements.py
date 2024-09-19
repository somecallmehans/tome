import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from achievements.models import Achievements


@pytest.mark.django_db(serialized_rollback=True)
def test_post_new_achievement():
    """Create a new achievement."""

    client = APIClient()
    url = reverse("upsert_achievements")

    payload = {
        "name": "Oops all soldiers",
        "description": "66 SOLDIERS",
        "point_value": 100,
    }

    response = client.post(url, payload, format="json")
    parsed_res = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert Achievements.objects.filter(id=parsed_res["id"]).exists()


@pytest.mark.django_db(serialized_rollback=True)
def test_post_update_new_achievement():
    """Update an existing achievement."""

    client = APIClient()
    url = reverse("upsert_achievements")

    payload = {
        "id": 1,
        "name": "Oops all elves",
        "description": "66 ELVES",
        "point_value": 6,
    }

    response = client.post(url, payload, format="json")
    parsed_res = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert parsed_res["name"] == "Oops all elves"
    assert Achievements.objects.get(id=parsed_res["id"]).name == "Oops all elves"
