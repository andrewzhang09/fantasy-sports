from flask import request, jsonify
from espn_api.basketball import League

from . import main_bp
from ..utils.project_matchup import project_matchup_handler
from ..utils.project_all import all_projections_handler
from ..utils.project_trade import project_trade_handler

@main_bp.route('/')
def home():
    return 'This is a fantasy sports helper, designed by Drew'

@main_bp.route('/submitHomeForm', methods=['POST'])
def submit_home_form():
    try:
        data = request.get_json()
        print('Received form data:', data)
        league_id, year, swid, espn_s2 = data.get('league_id'), data.get('year'), data.get('swid'), data.get('espn_s2')
        TT_LEAGUE = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)
        print(TT_LEAGUE.teams)
        response = jsonify({'success': True, 
                            'message': 'Form submitted successfully',
                            'teams': TT_LEAGUE.teams})
        return response
    except Exception as e:
        print('Error processing form data:', str(e))
        error_response = jsonify({'success': False, 
                                  'message': 'Error processing form data'})
        return error_response

@main_bp.route('/all-projections')
def all_projections_route():
    return all_projections_handler()

@main_bp.route('/project-matchup')
def project_matchup_route():
    return project_matchup_handler()

@main_bp.route('/project-trade')
def project_trade_route():
    return project_trade_handler()