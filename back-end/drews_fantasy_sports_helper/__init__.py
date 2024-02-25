# from flask import Flask, session
# from flask_cors import CORS
# from flask_pymongo import PyMongo

# def initialize_app():
#     app = Flask(__name__)
#     CORS(app)
#     app.config['MONGO_URI'] = 'mongodb://localhost:27017/fantasy_basketball_9_cat'
#     mongo = PyMongo(app)

#     with app.app_context():
#         from drews_fantasy_sports_helper.routes import main_bp
#         app.register_blueprint(main_bp)

#     return app
