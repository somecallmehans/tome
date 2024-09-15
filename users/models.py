from datetime import datetime

from django.db import models
from sessions_rounds.models import Rounds, Sessions
from achievements.models import Achievements


class Participants(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "participants"

    @property
    def total_points_current_month(self):
        today = datetime.today()
        mm_yy = today.strftime("%m-%y")

        total_points = ParticipantAchievements.objects.filter(
            participants=self.id,  # Filter by the current participant
            sessions__month_year=mm_yy,  # Filter by current session's month-year
        ).aggregate(total_points=models.Sum("achievements__point_value"))[
            "total_points"
        ]
        return total_points if total_points is not None else 0


class ParticipantAchievements(models.Model):
    participants = models.ForeignKey(Participants, on_delete=models.CASCADE)
    achievements = models.ForeignKey(Achievements, on_delete=models.CASCADE)
    rounds = models.ForeignKey(Rounds, on_delete=models.CASCADE)
    sessions = models.ForeignKey(Sessions, on_delete=models.CASCADE)

    class Meta:
        db_table = "participant_achievements"
