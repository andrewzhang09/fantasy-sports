from flask import current_app, jsonify
from espn_api.basketball import League

from .mongo_functions import create_team, create_league, get_teams


# saves the league and teams within MongoDB
def save_league_and_team_to_db(league_obj):
    teams = league_obj.teams
    teams_array = []
    for t in teams:
        team_dict = vars(t)
        # TODO: Roster and Schedule are not json serializable, so serialize them
        team_dict['roster'] = []
        team_dict['schedule'] = []
        team_dict['league_id'] = league_obj.league_id

        # insert team document into teams collection in MongoDB
        create_team(team_dict)
        teams_array.append(team_dict)

    create_league(league_obj.league_id, league_obj.year, teams_array)


def submit_home_form_handler(request):
    try:
        data = request.get_json()
        print('Received form data:', data)

        league_id, year, swid, espn_s2 = int(data.get('league_id')), int(data.get('year')), data.get('swid'), data.get('espn_s2')
        TT_LEAGUE = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)
        save_league_and_team_to_db(TT_LEAGUE)

        # check that they were saved
        print('League Teams: ')
        teams = get_teams()
        print([{'team_name': t.team_name, 'team_id': t.team_id, 'league_id': t.league_id} for t in teams])

        TEAM_MAP = {}
        # Only need the team names
        for team in TT_LEAGUE.teams:
            TEAM_MAP[team.team_id] = team.team_name

        response = jsonify({'success': True, 
                            'message': 'Form submitted successfully',
                            'teams': TEAM_MAP})
        return response
    except Exception as e:
        print('Error processing form data:', str(e))
        error_response = jsonify({'success': False, 
                                  'message': 'Error processing form data'})
        return error_response