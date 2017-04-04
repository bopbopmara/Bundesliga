import requests
from datetime import date

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
