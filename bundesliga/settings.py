import os

ALL_LEAGUES = [
    ('bl1', '1. Bundesliga'),
    ('bl2', '2. Bundesliga'),
    ('bl3', '3. Liga'),
]

ALLOWED_LEAGUES = os.environ.get('ALLOWED_LEAGUES', ' '.join([league[0] for league in ALL_LEAGUES])).split()

LEAGUES = [league for league in ALL_LEAGUES if league[0] in ALLOWED_LEAGUES]
