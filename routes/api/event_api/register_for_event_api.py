from modules.sql_manager import SqlManager
from flask import Blueprint, request

from modules.utiles.create_response import create_response
register_for_event_api_obj = Blueprint("register_for_event_api",__name__)


@register_for_event_api_obj.route("/event/register",methods=["GET"])
def fetch_events():
    try:
        event_id = request.get_json()["event_id"]
        name = request.get_json()["user_name"]
        school = request.get_json()["user_school"]
        grade = request.get_json()["user_grade"]
        dob = request.get_json()["user_dob"]
        contact = request.get_json()["user_contact"]
        with SqlManager().ClientEventHandler() as client_handler_object:
            all_events = client_handler_object.register_for_event(event_id,name,school,dob,grade,contact)
            return {"message":"fetched successfully","code":200,"data":all_events}
    except:
        return create_response(500,"Internal Server")