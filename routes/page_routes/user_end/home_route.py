from flask import Blueprint,render_template

user_home_blueprint = Blueprint("user_home",__name__)

@user_home_blueprint.route("/home")
def login():
    return render_template("/user_end/frontend.html")