from django.db import models


class Participants(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "participants"
