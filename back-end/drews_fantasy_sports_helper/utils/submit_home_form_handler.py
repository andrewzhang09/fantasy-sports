from flask import jsonify
from espn_api.basketball import League

from pprint import pprint

def submit_home_form_handler(request):
    # TODO: use Flask session to have the TT_LEAGUE object persist across API calls
    try:
        data = request.get_json()
        print('Received form data:', data)
        league_id, year, swid, espn_s2 = int(data.get('league_id')), int(data.get('year')), data.get('swid'), data.get('espn_s2')
        TT_LEAGUE = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)
        TEAM_MAP = {}
        for team in TT_LEAGUE.teams:
            team_dict = vars(team)
            # these attributes contain non serializable objects (players, matchups), so remove them
            del team_dict['roster']
            del team_dict['schedule']
            TEAM_MAP[team.team_id] = team_dict
        pprint(TEAM_MAP)
        response = jsonify({'success': True, 
                            'message': 'Form submitted successfully',
                            'teams': TEAM_MAP})
        return response
    except Exception as e:
        print('Error processing form data:', str(e))
        error_response = jsonify({'success': False, 
                                  'message': 'Error processing form data'})
        return error_response