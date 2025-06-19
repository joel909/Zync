from flask import Blueprint,render_template

login_api_obj = Blueprint("login_api",__name__)

@login_api_obj.route("/login")
def login_api():
    return render_template("login.html")