from dateutil.parser import parse

from flask import Flask
from flask import abort, render_template

from bundesliga import settings
from bundesliga.resources import (
    Match,
    Team,
    TeamStanding,
)
from bundesliga.utils.api import (
    build_statistics,
    retrieve_all_matches,
    retrieve_upcoming_matches,
)

app = Flask(__name__)


@app.route('/<league>/upcoming/')
def upcoming_matches(league):
    if league not in settings.ALLOWED_LEAGUES:
        abort(404)

    matches = [
        Match(
            host=Team(name=match_data['Team1']['TeamName'], image=match_data['Team1']['TeamIconUrl']),
            guest=Team(name=match_data['Team2']['TeamName'], image=match_data['Team2']['TeamIconUrl']),
            start_time=parse(match_data['MatchDateTimeUTC']),
        )
        for match_data in retrieve_upcoming_matches(league)
    ]

    return render_template('upcoming_matches.html', title='Upcoming', matches=matches)


@app.route('/<league>/all/')
def all_matches(league):
    if league not in settings.ALLOWED_LEAGUES:
        abort(404)

    matches_data, year = retrieve_all_matches(league)

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

    return render_template('all_matches.html', title='All', matches=matches)


@app.route('/')
@app.route('/<league>/')
def standings(league=None):
    if league is None and settings.ALLOWED_LEAGUES:
        league = settings.ALLOWED_LEAGUES[0]

    if league not in settings.ALLOWED_LEAGUES:
        abort(404)

    return render_template('standings.html', standings=sorted([
        TeamStanding(team_name, **team_statistics)
        for team_name, team_statistics in build_statistics(league).items()
    ], key=lambda team_standing: (-team_standing.points, -team_standing.difference)))
