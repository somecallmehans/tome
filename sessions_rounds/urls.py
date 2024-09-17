from django.urls import path
from .views import sessions_and_rounds, begin_round, close_round

urlpatterns = [
    path("sessions/", sessions_and_rounds, name="make_sessions_and_rounds"),
    path("begin_round/", begin_round, name="begin_round"),
    path("close_round", close_round, name="close_round"),
]
