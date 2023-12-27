from flask import Flask, session
from flask_cors import CORS
from flask_session import Session

def initialize_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    Session(app)

    from drews_fantasy_sports_helper.routes import main_bp
    app.register_blueprint(main_bp)

    return app
