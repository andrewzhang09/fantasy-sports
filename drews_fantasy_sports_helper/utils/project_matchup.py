from ..constants import ANDREW_ID, VIJAY_ID, FIRST_DAY, CATEGORIES, NINE_CATS, TEAM_MAP, TEAM_NAMES, AvgStatIntervals
from flask import render_template
from .helpers import get_projections

PLAYER_AVG_STAT_INTERVALS = AvgStatIntervals()

def project_matchup(id1, opponent_team_id, time_interval, ir, four_game_proj=False):
    # NOTE: ID1 IS YOUR TEAM
    # ex. time_interval: last 7, last 15
    # TODO: if current_matchup is True, add cats to current box score
    opponent_team_name = TEAM_MAP.get(opponent_team_id).get('team_name')
    print(TEAM_MAP.get(id1).get('team_name') + ' vs. ' + opponent_team_name)

    team1_projections = get_projections(id1, time_interval, ir, four_game_proj)
    team2_projections = get_projections(opponent_team_id, time_interval, ir, four_game_proj)
    print(time_interval)

    category_wins, category_ties, category_losses = 0, 0, 0
    MATCHUP_MAP = {}
    for cat in NINE_CATS:
        if team1_projections.get(cat) > team2_projections.get(cat):
            if cat == 'TO':
                category_losses += 1
            else:
                category_wins += 1
        elif team1_projections.get(cat) == team2_projections.get(cat):
            category_ties += 1
        else:
            if cat == 'TO':
                category_wins += 1
            else:
                category_losses += 1
        cat_diff = team1_projections.get(cat) - team2_projections.get(cat)
        MATCHUP_MAP[cat] = (round(team1_projections.get(cat), 4),
                            round(team2_projections.get(cat), 4),
                            round(cat_diff, 4))
    
    print(str(category_wins) + '-' + str(category_losses) + '-' + str(category_ties))
    MATCHUP_MAP['box_score'] = str(category_wins) + '-' + str(category_losses) + '-' + str(category_ties)
    return MATCHUP_MAP


# GET /project-matchup
def project_matchup_handler():
    MATCHUP_MAP = project_matchup(ANDREW_ID, 
                                  VIJAY_ID, 
                                  PLAYER_AVG_STAT_INTERVALS.LAST_30, 
                                  (None, 'Bradley Beal'))
    return render_template('project_matchup.html', 
                           matchup_map=MATCHUP_MAP, 
                           teams=[TEAM_NAMES.get(ANDREW_ID), TEAM_NAMES.get(VIJAY_ID)],
                           time_interval=PLAYER_AVG_STAT_INTERVALS.LAST_30,
                           nine_cats=NINE_CATS)