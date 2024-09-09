from rest_framework import serializers
from .models import Achievements, Restrictions

class RestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restrictions
        fields = ['id', 'name', 'url', 'nested']

class AchievementsSerializer(serializers.ModelSerializer):
    restrictions = RestrictionSerializer(many=True, read_only=True)

    class Meta:
        model = Achievements
        fields = ['id', 'name', 'description', 'point_value', 'parent_id', 'restrictions']
