from rest_framework import serializers
from .models import Participants

class ParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = '__all__'