from django.urls import path
from .views import (
    sessions_and_rounds,
    begin_round,
    close_round,
    sessions_and_rounds_by_date,
    all_sessions,
)

urlpatterns = [
    path(
        "sessions_by_date/",
        sessions_and_rounds_by_date,
        name="sessions-and-rounds-by-date",
    ),
    path("all_sessions/", all_sessions, name="all_sessions"),
    path("sessions/", sessions_and_rounds, name="make_sessions_and_rounds"),
    path("begin_round/", begin_round, name="begin_round"),
    path("close_round", close_round, name="close_round"),
]
