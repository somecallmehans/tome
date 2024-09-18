from users.models import ParticipantAchievements


def participant_achievement_factory(session, round, participant, achievement):
    ParticipantAchievements.objects.create(
        sessions=session,
        rounds=round,
        participants=participant,
        achievements=achievement,
    )
