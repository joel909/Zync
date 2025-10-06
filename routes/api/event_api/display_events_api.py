from flask import Blueprint
from modules.sql_manager import SqlManager
from modules.utiles.create_response import create_response


display_event_api_obj = Blueprint("display_event_api",__name__)
event_handler_object = SqlManager().EventHandler()

@display_event_api_obj.route("/event/get",method=["GET"])
def fetch_events():
    try:
        all_events = event_handler_object.get_all_events()
        return create_response(200,all_events)
    except:
        return create_response(500,"Internal Server")