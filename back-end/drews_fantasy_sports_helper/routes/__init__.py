from flask import Blueprint

main_bp = Blueprint('main', __name__)

from .main_routes import home, submit_home_form, all_projections_route, project_matchup_route, project_trade_route