from flask import Flask
from flask import abort, render_template

from bundesliga import settings
from bundesliga.utils.api import (
    build_statistics,
    retrieve_all_matches,
    retrieve_upcoming_matches,
)
from bundesliga.utils.app import (
    matches_from_data,
    standings_from_data,
)

app = Flask(__name__)


@app.route('/<league>/upcoming/')
def upcoming_matches(league):
    if league not in settings.ALLOWED_LEAGUES:
        abort(404)

    return render_template('upcoming_matches.html', title='Upcoming', matches=matches_from_data(retrieve_upcoming_matches(league)))


@app.route('/<league>/all/')
def all_matches(league):
    if league not in settings.ALLOWED_LEAGUES:
        abort(404)

    return render_template('all_matches.html', title='All', matches=matches_from_data(retrieve_all_matches(league)[0]))


@app.route('/')
@app.route('/<league>/')
def standings(league=None):
    if league is None and settings.ALLOWED_LEAGUES:
        league = settings.ALLOWED_LEAGUES[0]

    if league not in settings.ALLOWED_LEAGUES:
        abort(404)

    return render_template('standings.html', standings=standings_from_data(build_statistics(league)))
