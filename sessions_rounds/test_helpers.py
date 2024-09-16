from users.models import ParticipantAchievements

test_participants = [
    {"id": 1, "name": "Glennis Sansam"},
    {"id": 2, "name": "Sara Dewhurst"},
    {"id": 3, "name": "Uriel Cohani"},
    {"id": 4, "name": "Noella Gannon"},
]

test_participants_no_id = [
    {"name": "Celestia Clearie"},
    {"name": "Gilbert Loxton"},
    {"name": "Sammie Cruikshanks"},
]

combined_list = test_participants + test_participants_no_id


def participant_achievement_factory(session, round, participant, achievement):
    ParticipantAchievements.objects.create(
        sessions=session,
        rounds=round,
        participants=participant,
        achievements=achievement,
    )
