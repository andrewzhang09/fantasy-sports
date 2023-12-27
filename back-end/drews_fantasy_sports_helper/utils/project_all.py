from flask import jsonify, current_app, session
from .project_matchup import project_matchup
from ..constants import AvgStatIntervals

PLAYER_AVG_STAT_INTERVALS = AvgStatIntervals()

def generate_all_projections(id, time_interval):
    ALL_MATCHUPS = {}
    LEAGUE_TEAMS = session.get('TEAMS', [])
    print('League Teams: ', LEAGUE_TEAMS)
    for team in LEAGUE_TEAMS:
        opponent_team_id = team.team_id
        if opponent_team_id == id:
            continue
        matchup_map = project_matchup(id, 
                                      opponent_team_id, 
                                      time_interval,
                                      False)
        ALL_MATCHUPS[(id, opponent_team_id)] = matchup_map
        
    return ALL_MATCHUPS

# GET /all-projections
def all_projections_handler(request):
    team_id = request.args.get('teamId')
    time_interval = request.args.get('timeInterval')
    ALL_MATCHUPS = generate_all_projections(team_id, time_interval)

    response = jsonify({'success': True, 
                        'message': 'Form submitted successfully',
                        'matchup_map': ALL_MATCHUPS,
                        'time_intervals': vars(PLAYER_AVG_STAT_INTERVALS)})
    return response

    # return render_template('all_projections.html',
    #                        all_matchups=ALL_MATCHUPS,
    #                        team=TEAM_NAMES.get(ANDREW_ID),
    #                        time_interval=time_interval,
    #                        nine_cats=NINE_CATS,
    #                        team_names=TEAM_NAMES)
