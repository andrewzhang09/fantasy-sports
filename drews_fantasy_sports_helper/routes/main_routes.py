from flask import render_template
from . import main_bp
from ..utils.project_matchup import project_matchup
from ..utils.project_all import generate_all_projections
from ..constants import ANDREW_ID, VIJAY_ID, TEAM_MAP, TEAM_NAMES, NINE_CATS, AvgStatIntervals

PLAYER_AVG_STAT_INTERVALS = AvgStatIntervals()

## TODO: SCHEMA VALIDATION ##

@main_bp.route('/')
def home():
    return 'This is a fantasy sports helper, designed by Drew'

@main_bp.route('/all-projections')
def all_projections_handler():
    # generate_all_projections(id, time_interval)
    ALL_MATCHUPS = generate_all_projections(ANDREW_ID, PLAYER_AVG_STAT_INTERVALS.LAST_30)
    return render_template('all_projections.html',
                           all_matchups=ALL_MATCHUPS,
                           team=TEAM_NAMES.get(ANDREW_ID),
                           time_interval=PLAYER_AVG_STAT_INTERVALS.LAST_30,
                           nine_cats=NINE_CATS,
                           team_names=TEAM_NAMES)

@main_bp.route('/project-matchup')
def project_matchup_handler():
    # project_matchup(id1, opponent_team_id, time_interval, ir, four_game_proj=False)
    MATCHUP_MAP = project_matchup(ANDREW_ID, 
                                  VIJAY_ID, 
                                  PLAYER_AVG_STAT_INTERVALS.LAST_30, 
                                  (None, 'Bradley Beal'))
    return render_template('project_matchup.html', 
                           matchup_map=MATCHUP_MAP, 
                           teams=[TEAM_NAMES.get(ANDREW_ID), TEAM_NAMES.get(VIJAY_ID)],
                           time_interval=PLAYER_AVG_STAT_INTERVALS.LAST_30,
                           nine_cats=NINE_CATS)