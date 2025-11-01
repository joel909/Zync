from flask import Blueprint, render_template

registration_blueprint = Blueprint("registration", __name__)

@registration_blueprint.route("/dashboard/registration/<event_id>")
def registration(event_id):
    return render_template("admin_end/registration.html")
