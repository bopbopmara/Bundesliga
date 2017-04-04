from dateutil.parser import parse

from bundesliga.resources import (
    Match,
    Team,
    TeamStanding,
)


def matches_from_data(matches_data):
    matches = []
    for match_data in matches_data:
        match = Match(
            host=Team(name=match_data['Team1']['TeamName'], image=match_data['Team1']['TeamIconUrl']),
            guest=Team(name=match_data['Team2']['TeamName'], image=match_data['Team2']['TeamIconUrl']),
            start_time=parse(match_data['MatchDateTimeUTC']),
        )
        for result in match_data['MatchResults']:
            if result['ResultTypeID'] == 2:
                match.host_score = result['PointsTeam1']
                match.guest_score = result['PointsTeam2']
                break
        matches.append(match)

    return matches


def standings_from_data(statistics_data):
    standings = []
    for team_name, team_statistics in statistics_data.items():
        team_image = team_statistics.pop('image')
        standings.append(TeamStanding(Team(team_name, team_image), **team_statistics))

    return sorted(standings, key=lambda team_standing: (-team_standing.points, -team_standing.difference))
