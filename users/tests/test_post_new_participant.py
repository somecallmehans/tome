import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import Participants


@pytest.mark.django_db
def test_post_new_participant():
    client = APIClient()

    url = reverse("post_participant")

    payload = {"name": "John Newguy"}

    response = client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    participant_exists = Participants.objects.filter(name="John Newguy").exists()
    assert participant_exists


@pytest.mark.django_db(serialized_rollback=True)
def test_post_new_participant_fail():
    client = APIClient()

    url = reverse("post_participant")

    payload = {}

    response = client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
