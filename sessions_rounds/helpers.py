from users.models import Participants, ParticipantAchievements
from users.serializers import ParticipantsSerializer, ParticipantsAchievementsSerializer
from achievements.models import Achievements

PARTICIPATION_ACHIEVEMENT_ID = 24


def generate_pods(participants):
    """Generate pods of 4 or 3"""
    length = len(participants)
    if length in {1, 2, 5}:
        return [participants]

    pods = []
    mutate_ids = participants
    while length > 0:
        if length % 4 == 0 or length == 7 or (length - 4) >= 6:
            pods.append(mutate_ids[:4])
            mutate_ids = mutate_ids[4:]
            length -= 4
        else:
            pods.append(mutate_ids[:3])
            mutate_ids = mutate_ids[3:]
            length -= 3
    return pods


class RoundInformationService:
    def __init__(self, participants, session, round):
        self.participants = participants
        self.session = session
        self.round = round
        self.participation_achievement = Achievements.objects.get(
            id=PARTICIPATION_ACHIEVEMENT_ID
        )
        self.all_participants = []
        self.participant_data = []
        self.existing_participants = []
        self.new_participants = []
        self.participant_lookup = {}
        self.earned_participation_set = {}

    def categorize_participants(self):
        """Split up incoming participants into ones that exist and ones that don't"""
        self.existing_participants = [
            p for p in self.participants if p.get("id") is not None
        ]
        self.new_participants = [
            p for p in self.participants if p.get("id") is None and "name" in p
        ]

    def create_new_participants(self):
        """Take all of the new participants and make them into existing participants"""
        for p in self.new_participants:
            p_data = Participants.objects.create(name=p["name"])
            new_participant = ParticipantsSerializer(p_data)
            self.existing_participants.append(
                {"id": new_participant.data["id"], "name": new_participant.data["name"]}
            )

    def get_participants(self):
        """Get un-serialized Participants objects."""
        self.participant_data = Participants.objects.filter(
            id__in=[ep["id"] for ep in self.existing_participants]
        )

    def get_participants_serialized(self):
        """Serialize participants object."""
        all_serialized_participants = ParticipantsSerializer(
            self.participant_data, many=True
        )

        self.all_participants = all_serialized_participants.data

    def create_participants_lookup(self):
        """Create a lookup of the participants information."""
        self.participant_lookup = {p.id: p for p in self.participant_data}

    def get_session_achievement_data(self):
        """Get achievement data for the current session."""
        achievement_data = ParticipantAchievements.objects.filter(
            sessions_id=self.session.id, achievements_id=PARTICIPATION_ACHIEVEMENT_ID
        )
        earned_participation_achievements = ParticipantsAchievementsSerializer(
            achievement_data, many=True
        )
        self.earned_participation_set = {
            ea["participants"] for ea in earned_participation_achievements.data
        }

    def create_participation_achievements(self):
        """If someone hasn't gotten the participation achievement
        for the current session, they get one."""
        new_achievements = []
        for ep in self.existing_participants:
            if ep["id"] not in self.earned_participation_set:
                new_achievements.append(
                    ParticipantAchievements(
                        participants=self.participant_lookup[ep["id"]],
                        rounds=self.round,
                        sessions=self.session,
                        achievements=self.participation_achievement,
                    )
                )
        if len(new_achievements):
            ParticipantAchievements.objects.bulk_create(new_achievements)

    def build_participants_and_achievements(self):
        """Full process to get our stuff."""

        self.categorize_participants()

        self.create_new_participants()
        self.get_participants()

        self.create_participants_lookup()
        self.get_session_achievement_data()

        self.create_participation_achievements()

        self.get_participants_serialized()

        return self.all_participants
