from .project_matchup import project_matchup
from ..constants import IR_MAP

def generate_all_projections(id, time_interval):
    for opponent_team_id in range(1, 13):
        if opponent_team_id == id:
            continue
        print(project_matchup(id,
                               opponent_team_id,
                               time_interval,
                               (IR_MAP.get(id), IR_MAP.get(opponent_team_id)),
                               True))
        
    return {}