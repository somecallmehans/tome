import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_post_new_session_no_id():
    client = APIClient()

    url = reverse('make_sessions_and_rounds')

    payload = {
        'session_id': 111,
    }

    response = client.post(url, payload, format='json')

    assert response.status_code == status.HTTP_200_OK

    # assert response.status_code == status.HTTP_201_CREATED