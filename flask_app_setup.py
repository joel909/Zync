from flask import Flask
from routes.non_auth_routes.home_route import home_blueprint
from routes.non_auth_routes.login_route import login_blueprint
from routes.non_auth_routes.signup_route import signup_blueprint

from routes.api.auth_user import login_api_obj



def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(signup_blueprint)

    #API ROUTES
    app.register_blueprint(login_api_obj, url_prefix='/api')
    

    return app