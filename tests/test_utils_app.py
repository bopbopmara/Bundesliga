from datetime import datetime, timezone

from bundesliga.utils.app import (
    matches_from_data,
    standings_from_data,
)


def test_matches_from_data():
    assert matches_from_data([]) == []

    matches = matches_from_data([
        {
            'MatchDateTimeUTC': '2016-09-10T16:30:00Z',
            'Team1': {'TeamName': 'RB Leipzig', 'TeamIconUrl': 'http://www.sportal.de/photos/fussball/logos/35x35/1583.png'},
            'Team2': {'TeamName': 'Borussia Dortmund', 'TeamIconUrl': 'http://www.openligadb.de/images/teamicons/Borussia_Dortmund.gif'},
            'MatchIsFinished': True,
            'MatchResults': [
                {'PointsTeam1': 0, 'PointsTeam2': 0, 'ResultOrderID': 1, 'ResultTypeID': 1},
                {'PointsTeam1': 1, 'PointsTeam2': 0, 'ResultOrderID': 2, 'ResultTypeID': 2},
            ],
        },
    ])
    assert len(matches) == 1
    assert matches[0].start_time == datetime(2016, 9, 10, 16, 30, tzinfo=timezone.utc)
    assert matches[0].host.name == 'RB Leipzig'
    assert matches[0].guest.name == 'Borussia Dortmund'
    assert matches[0].host_score == 1
    assert matches[0].guest_score == 0


def test_standings_from_data():
    assert standings_from_data({}) == []

    standings = standings_from_data({
        '1. FC Union Berlin': {
            'points': 50,
            'wins': 15,
            'draws': 5,
            'losses': 6,
            'difference': 14,
        },
        'Eintracht Braunschweig': {
            'points': 50,
            'wins': 14,
            'draws': 8,
            'losses': 4,
            'difference': 14,
        },
        'Hannover 96': {
            'points': 49,
            'wins': 14,
            'draws': 7,
            'losses': 5,
            'difference': 13,
        },
        'VfB Stuttgart': {
            'points': 50,
            'wins': 15,
            'draws': 5,
            'losses': 6,
            'difference': 15,
        },
    })
    assert len(standings) == 4
    assert standings[0].name == 'VfB Stuttgart'
    assert standings[1].name in ['1. FC Union Berlin', 'Eintracht Braunschweig']
    assert standings[2].name in ['1. FC Union Berlin', 'Eintracht Braunschweig']
    assert standings[3].name == 'Hannover 96'
