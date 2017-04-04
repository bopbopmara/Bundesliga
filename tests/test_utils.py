from unittest.mock import patch

from freezegun import freeze_time

from bundesliga.utils import (
    retrieve_all_matches,
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
