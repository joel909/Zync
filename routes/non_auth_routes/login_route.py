from flask import Blueprint,render_template

blueprint_object = Blueprint("login",__name__)

@blueprint_object.route("/login")
def login():
    return render_template("login.html")