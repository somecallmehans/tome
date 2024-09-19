from django.urls import path
from .views import get_all_participants, upsert_participant

urlpatterns = [
    path("new_participant/", upsert_participant, name="upsert_participant"),
    path("participants/", get_all_participants, name="participant_list"),
]
