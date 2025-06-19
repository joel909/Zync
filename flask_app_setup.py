from flask import Flask
from routes.non_auth_routes.home_route import home_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_blueprint)
    return app