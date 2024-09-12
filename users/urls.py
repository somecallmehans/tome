from django.urls import path
from .views import get_all_participants, post_participant

urlpatterns = [
    path("new_participant/", post_participant, name="post_participant"),
    path("participants/", get_all_participants, name="participant_list"),
]
