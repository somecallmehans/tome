from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Achievements
from .serializers import AchievementsSerializer


@api_view(['GET'])
def get_achievements_with_restrictions(request):
    achievements = Achievements.objects.prefetch_related('restrictions')
    serializer = AchievementsSerializer(achievements, many=True)
    return Response(serializer.data)