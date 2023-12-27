from flask import current_app

def create_team(team_dict):
    with current_app.app_context():
        mongo = current_app.extensions.get('pymongo')
        mongo.db.teams.insert_one(team_dict)

def create_league(league_id, year, teams):
    league = { 
        'league_id': league_id,
        'year': year,
        'teams': teams
    }
    with current_app.app_context():
        mongo = current_app.extensions['pymongo']
        mongo.db.leagues.insert_one(league)

def get_teams():
    with current_app.app_context():
        mongo = current_app.extensions['pymongo']
        return mongo.db.teams.find()
