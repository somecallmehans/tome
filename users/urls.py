from django.urls import path
from .views import get_all_participants

urlpatterns = [
    path('participants/', get_all_participants, name='participant_list'),
]