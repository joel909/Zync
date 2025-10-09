from flask import Blueprint
from modules.sql_manager import SqlManager
from modules.utiles.create_response import create_response


display_event_api_obj = Blueprint("display_event_api",__name__)


@display_event_api_obj.route("/event/get",methods=["GET"])
def fetch_events():
    try:
        with SqlManager().EventHandler() as event_handler_object:
            all_events = event_handler_object.get_all_events()
            return {"message":"fetched successfully","code":200,"data":all_events}
    except:
        return create_response(500,"Internal Server")