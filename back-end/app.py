# from drews_fantasy_sports_helper import initialize_app
from flask import Flask, session
from flask_cors import CORS
from flask_pymongo import PyMongo

def initialize_app():
    app = Flask(__name__)
    CORS(app)
    # TODO: maybe this uri is wrong?
    # 2. maybe the flask version not compatible with flask-pymongo? Try regular pymongo instead?
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/fantasy_basketball_9_cat'
    mongo = PyMongo()
    mongo.init_app(app)

    with app.app_context():
        from drews_fantasy_sports_helper.routes import main_bp
        app.register_blueprint(main_bp)

    print(app.extensions)
    return app


if __name__ == '__main__':
    app = initialize_app()
    app.run(debug=True)