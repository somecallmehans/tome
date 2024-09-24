from rest_framework import serializers
from .models import Achievements, Restrictions


class RestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restrictions
        fields = ["id", "name", "url", "nested"]


class AchievementsSerializer(serializers.ModelSerializer):
    restrictions = RestrictionSerializer(many=True, read_only=True)
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Achievements
        fields = [
            "id",
            "name",
            "description",
            "point_value",
            "parent",
            "restrictions",
        ]

    def get_parent(self, obj):
        if obj.parent is not None:
            return AchievementsSerializer(obj.parent).data
        return None
