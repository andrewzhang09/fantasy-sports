from ..constants import ANDREW_ID, ALBERT_ID, CATEGORIES, NINE_CATS, TEAM_MAP, TEAM_NAMES, AvgStatIntervals, TT_LEAGUE
from flask import render_template
from .helpers import fetch_team, get_projections, calculate_fg_ft_percentage, fetch_curr_box_score, calculate_win_loss

from pprint import pprint

PLAYER_AVG_STAT_INTERVALS = AvgStatIntervals()

def project_matchup(id1, opponent_team_id, time_interval, is_curr_matchup=False, trade_dict={}):
    # NOTE: ID1 IS YOUR TEAM
    # ex. time_interval: last 7, last 15
    YOUR_TEAM = fetch_team(id1)
    OPPONENT_TEAM = fetch_team(opponent_team_id)
    opponent_team_name = OPPONENT_TEAM.team_name
    your_team_name = YOUR_TEAM.team_name
    print(your_team_name + ' vs. ' + opponent_team_name)
    
    MATCHUP_MAP = {}
    if is_curr_matchup:
        # fetch current box score
        fetch_curr_box_score(MATCHUP_MAP, id1)
        print('This is current box score: ')
        pprint(MATCHUP_MAP)

    # THESE INCLUDE FTM, FTA, ETC. CALCULATE AT THE END
    if not trade_dict:
        team1_projections = get_projections(id1, time_interval, is_curr_matchup)
        team2_projections = get_projections(opponent_team_id, time_interval, is_curr_matchup)
    else:
        # team1 is after trade, team2 is either your team before trade or an opponent team
        team1_projections = get_projections(id1, time_interval, is_curr_matchup, trade_dict)
        team2_projections = get_projections(opponent_team_id, time_interval, is_curr_matchup)

    print(time_interval)

    for cat in CATEGORIES:
        if is_curr_matchup:
            # for current matchup, add current stats to projections for rest of week
            curr_team1_stats, curr_team2_stats, _ = MATCHUP_MAP.get(cat, (0, 0, 0))
            proj_team1_total, proj_team2_total = curr_team1_stats + team1_projections.get(cat), curr_team2_stats + team2_projections.get(cat)
            if cat in ['FGM', 'FGA', 'FTM', 'FTA']:
                # cat diff does not matter because we are calculating ft% and fg%
                cat_diff = 0
            else:
                cat_diff = proj_team1_total - proj_team2_total 
            MATCHUP_MAP[cat] = (proj_team1_total, proj_team2_total, cat_diff)
        else:
            if cat in ['FGM', 'FGA', 'FTM', 'FTA']:
                cat_diff = 0
            else:
                cat_diff = team1_projections.get(cat) - team2_projections.get(cat)
            MATCHUP_MAP[cat] = (team1_projections.get(cat), team2_projections.get(cat), cat_diff)
    
    calculate_fg_ft_percentage(MATCHUP_MAP)
    category_wins, category_losses, category_ties = calculate_win_loss(MATCHUP_MAP)

    for cat in NINE_CATS:
        team1_stats, team2_stats, cat_diff = MATCHUP_MAP.get(cat)
        MATCHUP_MAP[cat] = (round(team1_stats, 4), round(team2_stats, 4), round(cat_diff, 4))
        
    MATCHUP_MAP['box_score'] = str(category_wins) + '-' + str(category_losses) + '-' + str(category_ties)
    pprint(MATCHUP_MAP)
    print(MATCHUP_MAP.get('box_score'))
    return MATCHUP_MAP


# GET /project-matchup
def project_matchup_handler():
    # TODO: change so that we don't manually have to code in inputs
    MATCHUP_MAP = project_matchup(ANDREW_ID, 
                                  ALBERT_ID, 
                                  PLAYER_AVG_STAT_INTERVALS.LAST_15,
                                  True)
    # TODO: add streaming candidates for each cat that you want to bolster
    return render_template('project_matchup.html', 
                           matchup_map=MATCHUP_MAP, 
                           teams=[TEAM_NAMES.get(ANDREW_ID), TEAM_NAMES.get(ALBERT_ID)],
                           time_interval=PLAYER_AVG_STAT_INTERVALS.LAST_15,
                           nine_cats=NINE_CATS)