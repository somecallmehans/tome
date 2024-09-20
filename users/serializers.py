from rest_framework import serializers
from .models import Participants, ParticipantAchievements


class ParticipantsSerializer(serializers.ModelSerializer):
    total_points = serializers.SerializerMethodField()

    class Meta:
        model = Participants
        fields = ["id", "name", "total_points"]

    def get_total_points(self, obj):
        mm_yy = self.context.get("mm_yy", None)
        return obj.get_total_points(mm_yy)


class ParticipantsAchievementsSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(read_only=True)
    sessions = serializers.PrimaryKeyRelatedField(read_only=True)
    rounds = serializers.PrimaryKeyRelatedField(read_only=True)
    achievements = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ParticipantAchievements
        fields = ["id", "participants", "achievements", "rounds", "sessions"]
