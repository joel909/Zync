from flask import Flask
from routes.non_auth_routes.dashboard_route import home_blueprint
from routes.non_auth_routes.login_route import login_blueprint
from routes.non_auth_routes.signup_route import signup_blueprint

from routes.api.auth_api.login_api import login_api_obj
from routes.api.auth_api.sign_up_api import signup_api_obj
from routes.api.event_api.create_event_api import create_event_api_obj

from routes.middleware.auth import authenticate_user
from flask import Blueprint, request, g



def create_app():
    app = Flask(__name__)
    #middleware 
    @app.before_request
    def auth_user():
        if authenticate_user() == True:
            pass
        else:
            return "Unauthorized please re-login to continue", 401


    app.register_blueprint(home_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(signup_blueprint)


    #API ROUTES
    #login api
    app.register_blueprint(login_api_obj, url_prefix='/api')

    #signup-api
    app.register_blueprint(signup_api_obj,url_prefix='/api')

    ##create even API
    app.register_blueprint(create_event_api_obj,url_prefix="/api")

    print("all the registered endpoints are : ",app.url_map)
    

    return app