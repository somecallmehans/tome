import pytest
from sessions_rounds.test_helpers import test_participants
from users.models import Participants


@pytest.fixture(scope="session")
def create_base_participants(django_db_setup, django_db_blocker):
    base_participants = []
    with django_db_blocker.unblock():
        for p in test_participants:
            p = Participants.objects.create(name=p["name"])
            base_participants.append(p)
    return base_participants
