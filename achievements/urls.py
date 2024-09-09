from django.urls import path
from .views import get_achievements_with_restrictions

urlpatterns = [
    path('achievements_restrictions/', get_achievements_with_restrictions, name='achievements_restrictions_list')
]