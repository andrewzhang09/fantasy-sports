from . import main_bp
from ..utils.project_matchup import project_matchup_handler
from ..utils.project_all import all_projections_handler
from ..utils.project_trade import project_trade_handler

@main_bp.route('/')
def home():
    return 'This is a fantasy sports helper, designed by Drew'

@main_bp.route('/all-projections')
def all_projections_route():
    return all_projections_handler()

@main_bp.route('/project-matchup')
def project_matchup_route():
    return project_matchup_handler()

@main_bp.route('/project-trade')
def project_trade_route():
    return project_trade_handler()