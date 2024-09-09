from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Participants
from .serializers import ParticipantsSerializer


@api_view(['GET'])
def get_all_participants(request):
    participants = Participants.objects.all().filter(deleted=False)
    serializer = ParticipantsSerializer(participants, many=True)
    return Response(serializer.data)