from django.db import models


class Restrictions(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)
    nested = models.BooleanField(default=False)

    class Meta:
        db_table = "restrictions"


class Achievements(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    point_value = models.IntegerField()
    deleted = models.BooleanField(default=False)
    parent_id = models.IntegerField(null=True)

    restrictions = models.ManyToManyField(
        "Restrictions", through="AchievementsRestrictions"
    )

    class Meta:
        db_table = "achievements"


class AchievementsRestrictions(models.Model):
    achievements = models.ForeignKey(Achievements, on_delete=models.CASCADE)
    restrictions = models.ForeignKey(Restrictions, on_delete=models.CASCADE)

    class Meta:
        db_table = "achievements_restrictions"
