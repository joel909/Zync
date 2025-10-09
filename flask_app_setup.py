from flask import Flask
#Admin
from routes.page_routes.admin_end.dashboard_route import home_blueprint
from routes.page_routes.admin_end.login_route import login_blueprint
from routes.page_routes.admin_end.signup_route import signup_blueprint

#User
from routes.page_routes.user_end.home_route import user_home_blueprint

from routes.api.auth_api.login_api import login_api_obj
from routes.api.auth_api.sign_up_api import signup_api_obj
from routes.api.event_api.create_event_api import create_event_api_obj
from routes.api.event_api.display_events_api import display_event_api_obj


from routes.middleware.auth import authenticate_user
from flask import Blueprint, request, g,redirect,url_for    



def create_app():
    app = Flask(__name__)
    #middleware 
    @app.before_request
    def auth_user():
        if authenticate_user() == True:
            if request.path == "/admin/signup":
                print("redirecting")
                return redirect("/admin/dashboard")
        else:
            return "Unauthorized please re-login to continue", 401

    #ADMIM END
    app.register_blueprint(home_blueprint,url_prefix='/admin')
    app.register_blueprint(login_blueprint,url_prefix='/admin')
    app.register_blueprint(signup_blueprint,url_prefix='/admin')

    #NORMAL USER END
    app.register_blueprint(user_home_blueprint)


    #API ROUTES
    #login api
    app.register_blueprint(login_api_obj, url_prefix='/api')

    #signup-api
    app.register_blueprint(signup_api_obj,url_prefix='/api')

    #get all user related events
    app.register_blueprint(display_event_api_obj,url_prefix='/admin/api')

    ##create event API
    app.register_blueprint(create_event_api_obj,url_prefix="/api")

    print("all the registered endpoints are : ",app.url_map)
    

    return app