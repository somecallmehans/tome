from django.urls import path
from .views import make_sessions_and_rounds

urlpatterns = [
    path('sessions/', make_sessions_and_rounds, name='make_sessions_and_rounds')
]