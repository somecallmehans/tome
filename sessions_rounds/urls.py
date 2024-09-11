from django.urls import path
from .views import sessions_and_rounds

urlpatterns = [path("sessions/", sessions_and_rounds, name="make_sessions_and_rounds")]
