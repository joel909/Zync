from flask import Blueprint,render_template

login_blueprint = Blueprint("login",__name__)

@login_blueprint.route("/login")
def login():
    return render_template("/admin_end/login.html")