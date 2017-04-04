import requests
from datetime import date

POINTS_WIN = 3

POINTS_DRAW = 1

matchday_url = lambda league: 'https://www.openligadb.de/api/getcurrentgroup/{}'.format(league)

matches_for_league_url = lambda league, year: 'https://www.openligadb.de/api/getmatchdata/{league}/{year}'.format(
    league=league,
    year=year,
)

matches_for_matchday_url = lambda league, year, matchday: 'https://www.openligadb.de/api/getmatchdata/{league}/{year}/{matchday}'.format(
    league=league,
    year=year,
    matchday=matchday,
)

teams_for_league_url = lambda league, year: 'https://www.openligadb.de/api/getavailableteams/{league}/{year}'.format(
    league=league,
    year=year,
)


def retrieve_upcoming_matches(league):
    # Retrieve data for current matchday
    response = requests.get(matchday_url(league))
    if response.status_code != 200:
        return []

    matchday = response.json()['GroupOrderID']

    # Try to retrieve matches for current matchday
    # for the tournament edition that started this year
    year = date.today().year
    response = requests.get(matches_for_matchday_url(league, year, matchday))
    if response.status_code != 200:
        return []

    matches_data = response.json()

    # If no matches are found we're probably at the second
    # half of the tournament edition that started last year
    if not matches_data:
        year -= 1
        response = requests.get(matches_for_matchday_url(league, year, matchday))
        if response.status_code != 200:
            return []

        matches_data = response.json()

    # If all matches for the current matchday have already ended
    # we actually need to retrieve matches for the next matchday
    if matches_data and all([match_data['MatchIsFinished'] for match_data in matches_data]):
        matchday += 1
        response = requests.get(matches_for_matchday_url(league, year, matchday))
        if response.status_code != 200:
            return []

        matches_data = response.json()

    return matches_data


def retrieve_all_matches(league):
    # Try to retrieve matches for the tournament edition that started this year
    year = date.today().year
    response = requests.get(matches_for_league_url(league, year))
    if response.status_code != 200:
        return [], None

    matches_data = response.json()

    # If no matches are found we're probably at the second
    # half of the tournament edition that started last year
    if not matches_data:
        year -= 1
        response = requests.get(matches_for_league_url(league, year))
        if response.status_code != 200:
            return [], None

        matches_data = response.json()

    return matches_data, year


def retrieve_all_teams(league, year):
    response = requests.get(teams_for_league_url(league, year))
    if response.status_code != 200:
        return []

    return response.json()


def build_statistics(league):
    matches_data, year = retrieve_all_matches(league)

    statistics = {
        team['TeamName']: {'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'difference': 0}
        for team in retrieve_all_teams(league, year)
    }

    for match_data in matches_data:
        if not match_data['MatchIsFinished']:
            break

        host_name = match_data['Team1']['TeamName']
        guest_name = match_data['Team2']['TeamName']
        host_score, guest_score = None, None

        for result in match_data['MatchResults']:
            if result['ResultTypeID'] == 2:
                host_score = result['PointsTeam1']
                guest_score = result['PointsTeam2']
                break

        if host_score > guest_score:
            statistics[host_name]['wins'] += 1
            statistics[host_name]['points'] += POINTS_WIN
            statistics[host_name]['difference'] += (host_score - guest_score)
            statistics[guest_name]['losses'] += 1
            statistics[guest_name]['difference'] += (guest_score - host_score)
        elif host_score < guest_score:
            statistics[guest_name]['wins'] += 1
            statistics[guest_name]['points'] += POINTS_WIN
            statistics[guest_name]['difference'] += (guest_score - host_score)
            statistics[host_name]['losses'] += 1
            statistics[host_name]['difference'] += (host_score - guest_score)
        else:
            statistics[host_name]['draws'] += 1
            statistics[host_name]['points'] += POINTS_DRAW
            statistics[guest_name]['draws'] += 1
            statistics[guest_name]['points'] += POINTS_DRAW

    return statistics
