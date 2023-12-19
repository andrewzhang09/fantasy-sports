from flask import Flask

app = Flask(__name__)

from drews_fantasy_sports_helper.routes import main_bp

app.register_blueprint(main_bp)

import drews_fantasy_sports_helper.routes
