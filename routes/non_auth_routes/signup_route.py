from flask import Blueprint,render_template

signup_blueprint = Blueprint("signup",__name__)

@signup_blueprint.route("/signup")
def signup():
    return render_template("signup.html")