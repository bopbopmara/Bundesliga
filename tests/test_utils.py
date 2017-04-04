from unittest.mock import patch

from freezegun import freeze_time

from bundesliga.utils import (
    build_statistics,
    retrieve_all_matches,
    retrieve_all_teams,
    retrieve_upcoming_matches,
)


class APIResponse(object):
    def __init__(self, status_code=200, content=None):
        self.status_code = status_code
        self.content = content

    def json(self):
        return self.content


@freeze_time('2017-06-01')
def test_retrieve_upcoming_matches():
    # Current matchday retrieval fails
    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getcurrentgroup/bl1':
            return APIResponse(status_code=500)

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_upcoming_matches('bl1') == []

    # The upcoming matches are for the current matchday of the tournament edition that started this year
    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getcurrentgroup/bl1':
            return APIResponse(content={'GroupOrderID': 2})
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017/2':
            return APIResponse(status_code=500)

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_upcoming_matches('bl1') == []

    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getcurrentgroup/bl1':
            return APIResponse(content={'GroupOrderID': 2})
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017/2':
            return APIResponse(content=[
                {
                    'MatchDateTimeUTC': '2017-06-26T18:30:00Z',
                    'MatchIsFinished': False,
                },
                {
                    'MatchDateTimeUTC': '2017-06-26T20:00:00Z',
                    'MatchIsFinished': True,
                },
            ])

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_upcoming_matches('bl1') == [
            {
                'MatchDateTimeUTC': '2017-06-26T18:30:00Z',
                'MatchIsFinished': False,
            },
            {
                'MatchDateTimeUTC': '2017-06-26T20:00:00Z',
                'MatchIsFinished': True,
            },
        ]

    # The upcoming matches are for the next matchday of the tournament edition that started this year
    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getcurrentgroup/bl1':
            return APIResponse(content={'GroupOrderID': 2})
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017/2':
            return APIResponse(content=[
                {
                    'MatchDateTimeUTC': '2017-05-26T18:30:00Z',
                    'MatchIsFinished': True,
                },
                {
                    'MatchDateTimeUTC': '2017-05-26T20:00:00Z',
                    'MatchIsFinished': True,
                },
            ])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017/3':
            return APIResponse(status_code=500)

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_upcoming_matches('bl1') == []

    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getcurrentgroup/bl1':
            return APIResponse(content={'GroupOrderID': 2})
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017/2':
            return APIResponse(content=[
                {
                    'MatchDateTimeUTC': '2017-05-26T18:30:00Z',
                    'MatchIsFinished': True,
                },
                {
                    'MatchDateTimeUTC': '2017-05-26T20:00:00Z',
                    'MatchIsFinished': True,
                },
            ])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017/3':
            return APIResponse(content=[
                {
                    'MatchDateTimeUTC': '2017-06-26T18:30:00Z',
                    'MatchIsFinished': False,
                },
            ])

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_upcoming_matches('bl1') == [
            {
                'MatchDateTimeUTC': '2017-06-26T18:30:00Z',
                'MatchIsFinished': False,
            },
        ]

    # The upcoming matches are for the current matchday of the tournament edition that started last year
    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getcurrentgroup/bl1':
            return APIResponse(content={'GroupOrderID': 2})
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017/2':
            return APIResponse(content=[])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2016/2':
            return APIResponse(status_code=500)

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_upcoming_matches('bl1') == []

    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getcurrentgroup/bl1':
            return APIResponse(content={'GroupOrderID': 2})
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017/2':
            return APIResponse(content=[])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2016/2':
            return APIResponse(content=[
                {
                    'MatchDateTimeUTC': '2017-06-26T18:30:00Z',
                    'MatchIsFinished': True,
                },
                {
                    'MatchDateTimeUTC': '2017-06-26T20:00:00Z',
                    'MatchIsFinished': False,
                },
            ])

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_upcoming_matches('bl1') == [
            {
                'MatchDateTimeUTC': '2017-06-26T18:30:00Z',
                'MatchIsFinished': True,
            },
            {
                'MatchDateTimeUTC': '2017-06-26T20:00:00Z',
                'MatchIsFinished': False,
            },
        ]

    # The upcoming matches are for the next matchday of the tournament edition that started last year
    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getcurrentgroup/bl1':
            return APIResponse(content={'GroupOrderID': 2})
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017/2':
            return APIResponse(content=[])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2016/2':
            return APIResponse(content=[
                {
                    'MatchDateTimeUTC': '2017-05-26T18:30:00Z',
                    'MatchIsFinished': True,
                },
                {
                    'MatchDateTimeUTC': '2017-05-26T20:00:00Z',
                    'MatchIsFinished': True,
                },
            ])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2016/3':
            return APIResponse(status_code=500)

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_upcoming_matches('bl1') == []

    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getcurrentgroup/bl1':
            return APIResponse(content={'GroupOrderID': 2})
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017/2':
            return APIResponse(content=[])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2016/2':
            return APIResponse(content=[
                {
                    'MatchDateTimeUTC': '2017-05-26T18:30:00Z',
                    'MatchIsFinished': True,
                },
                {
                    'MatchDateTimeUTC': '2017-05-26T20:00:00Z',
                    'MatchIsFinished': True,
                },
            ])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2016/3':
            return APIResponse(content=[
                {
                    'MatchDateTimeUTC': '2017-06-26T18:30:00Z',
                    'MatchIsFinished': False,
                },
            ])

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_upcoming_matches('bl1') == [
            {
                'MatchDateTimeUTC': '2017-06-26T18:30:00Z',
                'MatchIsFinished': False,
            },
        ]


@freeze_time('2017-06-01')
def test_retrieve_all_matches():
    # The matches are for the tournament edition that started this year
    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017':
            return APIResponse(status_code=500)

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_all_matches('bl1') == ([], None)

    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017':
            return APIResponse(content=[
                {
                    'MatchDateTimeUTC': '2017-06-26T18:30:00Z',
                    'MatchIsFinished': True,
                },
                {
                    'MatchDateTimeUTC': '2017-07-26T20:00:00Z',
                    'MatchIsFinished': False,
                },
            ])

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_all_matches('bl1') == ([
            {
                'MatchDateTimeUTC': '2017-06-26T18:30:00Z',
                'MatchIsFinished': True,
            },
            {
                'MatchDateTimeUTC': '2017-07-26T20:00:00Z',
                'MatchIsFinished': False,
            },
        ], 2017)

    # The matches are for the tournament edition that started last year
    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017':
            return APIResponse(content=[])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2016':
            return APIResponse(status_code=500)

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_all_matches('bl1') == ([], None)

    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017':
            return APIResponse(content=[])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2016':
            return APIResponse(content=[
                {
                    'MatchDateTimeUTC': '2016-06-26T18:30:00Z',
                    'MatchIsFinished': True,
                },
                {
                    'MatchDateTimeUTC': '2017-06-26T20:00:00Z',
                    'MatchIsFinished': False,
                },
            ])

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_all_matches('bl1') == ([
            {
                'MatchDateTimeUTC': '2016-06-26T18:30:00Z',
                'MatchIsFinished': True,
            },
            {
                'MatchDateTimeUTC': '2017-06-26T20:00:00Z',
                'MatchIsFinished': False,
            },
        ], 2016)


def test_retrieve_teams():
    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getavailableteams/bl1/2016':
            return APIResponse(status_code=500)

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_all_teams('bl1', 2016) == []

    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getavailableteams/bl1/2016':
            return APIResponse(content=[
                {'TeamName': 'Borussia Dortmund'},
                {'TeamName': 'Bayern München'},
                {'TeamName': 'RB Leipzig'},
            ])

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        assert retrieve_all_teams('bl1', 2016) == [
            {'TeamName': 'Borussia Dortmund'},
            {'TeamName': 'Bayern München'},
            {'TeamName': 'RB Leipzig'},
        ]


@freeze_time('2017-06-01')
def test_build_statistics():
    def requests_get(url):
        if url == 'https://www.openligadb.de/api/getavailableteams/bl1/2016':
            return APIResponse(content=[
                {'TeamName': 'Borussia Dortmund'},
                {'TeamName': 'Bayern München'},
                {'TeamName': 'RB Leipzig'},
                {'TeamName': 'SV Darmstadt 98'},
            ])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2017':
            return APIResponse(content=[])
        if url == 'https://www.openligadb.de/api/getmatchdata/bl1/2016':
            return APIResponse(content=[
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
                {
                    'MatchDateTimeUTC': '2016-11-19T17:30:00Z',
                    'Team1': {'TeamName': 'Borussia Dortmund', 'TeamIconUrl': 'http://www.openligadb.de/images/teamicons/Borussia_Dortmund.gif'},
                    'Team2': {'TeamName': 'Bayern München', 'TeamIconUrl': 'http://www.openligadb.de/images/teamicons/Bayern_Muenchen.gif'},
                    'MatchIsFinished': True,
                    'MatchResults': [
                        {'PointsTeam1': 1, 'PointsTeam2': 0, 'ResultOrderID': 1, 'ResultTypeID': 1},
                        {'PointsTeam1': 1, 'PointsTeam2': 0, 'ResultOrderID': 2, 'ResultTypeID': 2},
                    ],
                },
                {
                    'MatchDateTimeUTC': '2016-12-21T19:00:00Z',
                    'Team1': {'TeamName': 'Bayern München', 'TeamIconUrl': 'http://www.openligadb.de/images/teamicons/Bayern_Muenchen.gif'},
                    'Team2': {'TeamName': 'RB Leipzig', 'TeamIconUrl': 'http://www.sportal.de/photos/fussball/logos/35x35/1583.png'},
                    'MatchIsFinished': True,
                    'MatchResults': [
                        {'PointsTeam1': 3, 'PointsTeam2': 0, 'ResultOrderID': 1, 'ResultTypeID': 1},
                        {'PointsTeam1': 3, 'PointsTeam2': 0, 'ResultOrderID': 2, 'ResultTypeID': 2},
                    ],
                },
                {
                    'MatchDateTimeUTC': '2017-02-04T17:30:00Z',
                    'Team1': {'TeamName': 'Borussia Dortmund', 'TeamIconUrl': 'http://www.openligadb.de/images/teamicons/Borussia_Dortmund.gif'},
                    'Team2': {'TeamName': 'RB Leipzig', 'TeamIconUrl': 'http://www.sportal.de/photos/fussball/logos/35x35/1583.png'},
                    'MatchIsFinished': True,
                    'MatchResults': [
                        {'PointsTeam1': 1, 'PointsTeam2': 0, 'ResultOrderID': 1, 'ResultTypeID': 1},
                        {'PointsTeam1': 1, 'PointsTeam2': 0, 'ResultOrderID': 2, 'ResultTypeID': 2},
                    ],
                },
                {
                    'MatchDateTimeUTC': '2017-04-08T16:30:00Z',
                    'Team1': {'TeamName': 'Bayern München', 'TeamIconUrl': 'http://www.openligadb.de/images/teamicons/Bayern_Muenchen.gif'},
                    'Team2': {'TeamName': 'Borussia Dortmund', 'TeamIconUrl': 'http://www.openligadb.de/images/teamicons/Borussia_Dortmund.gif'},
                    'MatchIsFinished': True,
                    'MatchResults': [
                        {'PointsTeam1': 1, 'PointsTeam2': 0, 'ResultOrderID': 1, 'ResultTypeID': 1},
                        {'PointsTeam1': 1, 'PointsTeam2': 1, 'ResultOrderID': 2, 'ResultTypeID': 2},
                    ],
                },
                {
                    'MatchDateTimeUTC': '2017-05-13T13:30:00Z',
                    'Team1': {'TeamName': 'RB Leipzig', 'TeamIconUrl': 'http://www.sportal.de/photos/fussball/logos/35x35/1583.png'},
                    'Team2': {'TeamName': 'Bayern München', 'TeamIconUrl': 'http://www.openligadb.de/images/teamicons/Bayern_Muenchen.gif'},
                    'MatchIsFinished': False,
                    'MatchResults': [],
                },
            ])

    with patch('bundesliga.utils.requests.get', side_effect=requests_get):
        statistics = build_statistics('bl1')

    assert len(statistics.keys()) == 4
    assert statistics['Borussia Dortmund'] == {
        'wins': 2,
        'draws': 1,
        'losses': 1,
        'points': 7,
        'difference': 1,
    }
    assert statistics['Bayern München'] == {
        'wins': 1,
        'draws': 1,
        'losses': 1,
        'points': 4,
        'difference': 2,
    }
    assert statistics['RB Leipzig'] == {
        'wins': 1,
        'draws': 0,
        'losses': 2,
        'points': 3,
        'difference': -3,
    }
    assert statistics['SV Darmstadt 98'] == {
        'wins': 0,
        'draws': 0,
        'losses': 0,
        'points': 0,
        'difference': 0,
    }
