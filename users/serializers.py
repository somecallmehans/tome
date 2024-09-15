from rest_framework import serializers
from .models import Participants, ParticipantAchievements


class ParticipantsSerializer(serializers.ModelSerializer):
    total_points_current_month = serializers.ReadOnlyField()

    class Meta:
        model = Participants
        fields = ["id", "name", "total_points_current_month"]


class ParticipantsAchievementsSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(read_only=True)
    sessions = serializers.PrimaryKeyRelatedField(read_only=True)
    rounds = serializers.PrimaryKeyRelatedField(read_only=True)
    achievements = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ParticipantAchievements
        fields = ["id", "participants", "achievements", "rounds", "sessions"]
