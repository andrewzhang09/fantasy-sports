from flask import render_template
from .project_matchup import project_matchup
from ..constants import ANDREW_ID, IR_MAP, NINE_CATS, TEAM_NAMES, AvgStatIntervals

PLAYER_AVG_STAT_INTERVALS = AvgStatIntervals()

def generate_all_projections(id, time_interval):
    ALL_MATCHUPS = {}
    for opponent_team_id in range(1, 13):
        if opponent_team_id == id:
            continue
        matchup_map = project_matchup(id, 
                                      opponent_team_id, 
                                      time_interval, 
                                      (IR_MAP.get(id), IR_MAP.get(opponent_team_id)), 
                                      False)
        ALL_MATCHUPS[(id, opponent_team_id)] = matchup_map
        
    return ALL_MATCHUPS

# GET /all-projections
def all_projections_handler():
    # generate_all_projections(id, time_interval)
    # TODO: change so we don't have to manually code the inputs
    ALL_MATCHUPS = generate_all_projections(ANDREW_ID, PLAYER_AVG_STAT_INTERVALS.LAST_30)
    return render_template('all_projections.html',
                           all_matchups=ALL_MATCHUPS,
                           team=TEAM_NAMES.get(ANDREW_ID),
                           time_interval=PLAYER_AVG_STAT_INTERVALS.LAST_30,
                           nine_cats=NINE_CATS,
                           team_names=TEAM_NAMES)
