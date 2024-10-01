from django.urls import path
from .views import (
    get_achievements_with_restrictions,
    post_achievements_for_participants,
    upsert_achievements,
    get_colors,
)

urlpatterns = [
    path("upsert_achievements/", upsert_achievements, name="upsert_achievements"),
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
    path("colors/", get_colors, name="colors"),
]
