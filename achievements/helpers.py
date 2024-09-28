from achievements.models import Achievements
from users.models import Participants, ParticipantAchievements
from sessions_rounds.models import Sessions, Rounds


class AchievementCleaverService:
    def __init__(self, participants, session, round):
        self.participants = participants
        self.session = Sessions.objects.get(id=session)
        self.round = Rounds.objects.get(id=round)
        self.achievements_lookup = {}
        self.participants_lookup = {}

    def create_achievements_lookup(self):
        """Get all the achievements, make a lookup."""
        achievement_data = Achievements.objects.all()
        self.achievements_lookup = {a.id: a for a in achievement_data}

    def create_participants_lookup(self):
        """Get the participant data and make a lookup."""
        participant_data = Participants.objects.filter(
            id__in=[p["participant"] for p in self.participants]
        )
        self.participants_lookup = {p.id: p for p in participant_data}

    def build_lookups(self):
        """Build some lookups."""
        self.create_achievements_lookup()
        self.create_participants_lookup()

    def build_service(self):
        """Full process of logging achievements."""
        self.build_lookups()

        for item in self.participants:
            for achievement in item["achievements"]:
                ParticipantAchievements.objects.create(
                    participant=self.participants_lookup[item["participant"]],
                    achievement=self.achievements_lookup[achievement],
                    session=self.session,
                    round=self.round,
                )


def make_achievement_map(achievements):
    achievement_map = {}
    for achievement in achievements:
        if achievement["parent"] is None:
            achievement_with_children = {
                **achievement,
                "children": [],
            }
            point_value = achievement["point_value"]
            if point_value not in achievement_map:
                achievement_map[point_value] = []

            achievement_map[point_value].append(achievement_with_children)
        else:
            parent_achievement = achievement["parent"]

            parent_point_value = parent_achievement["point_value"]
            for parent in achievement_map.get(parent_point_value, []):
                if parent["id"] == parent_achievement["id"]:
                    parent["children"].append(achievement)

    return achievement_map
