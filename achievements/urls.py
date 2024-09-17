from django.urls import path
from .views import (
    get_achievements_with_restrictions,
    post_achievements_for_participants,
)

urlpatterns = [
    path(
        "submit_achievements/",
        post_achievements_for_participants,
        name="submit_achievements",
    ),
    path(
        "achievements_restrictions/",
        get_achievements_with_restrictions,
        name="achievements_restrictions_list",
    ),
]
