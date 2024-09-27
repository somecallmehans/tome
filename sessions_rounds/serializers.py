from rest_framework import serializers
from .models import Sessions, Rounds


class RoundsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rounds
        fields = ["id", "round_number", "completed", "deleted"]


class SessionSerializer(serializers.ModelSerializer):
    rounds = RoundsSerializer(many=True, read_only=True, source="rounds_set")

    class Meta:
        model = Sessions
        fields = ["id", "month_year", "closed", "deleted", "rounds"]
