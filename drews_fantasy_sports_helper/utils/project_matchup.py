from ..constants import FIRST_DAY, CATEGORIES, NINE_CATS, TEAM_MAP
from .helpers import get_projections

def project_matchup(id1, opponent_team_id, time_interval, ir, four_game_proj=False):
    # NOTE: ID1 IS YOUR TEAM
    # ex. time_interval: last 7, last 15

    # else:
    #     opponent_team_id = get_opponent_team_id(id1, matchup_num)
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