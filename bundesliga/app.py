from flask import Flask
from flask import abort, render_template

from bundesliga import settings
from bundesliga.utils.api import (
    build_statistics,
    retrieve_all_matches,
    retrieve_upcoming_matches,
)
from bundesliga.utils.app import (
    league_name,
    matches_from_data,
    standings_from_data,
)

app = Flask(__name__)


@app.route('/<league>/upcoming/')
def upcoming_matches(league):
    if league not in settings.ALLOWED_LEAGUES:
        abort(404)

    context = {
        'title': 'Upcoming Matches: {}'.format(league_name(league)),
        'matches': matches_from_data(retrieve_upcoming_matches(league)),
        'leagues': settings.LEAGUES,
    }
    return render_template('matches.html', **context)


@app.route('/<league>/all/')
def all_matches(league):
    if league not in settings.ALLOWED_LEAGUES:
        abort(404)

    context = {
        'title': 'All Matches: {}'.format(league_name(league)),
        'matches': matches_from_data(retrieve_all_matches(league)[0]),
        'leagues': settings.LEAGUES,
    }
    return render_template('matches.html', **context)


@app.route('/')
@app.route('/<league>/')
def standings(league=None):
    if league is None and settings.ALLOWED_LEAGUES:
        league = settings.ALLOWED_LEAGUES[0]

    if league not in settings.ALLOWED_LEAGUES:
        abort(404)

    context = {
        'title': 'Standings: {}'.format(league_name(league)),
        'standings': standings_from_data(build_statistics(league)),
        'leagues': settings.LEAGUES,
    }
    return render_template('standings.html', **context)
