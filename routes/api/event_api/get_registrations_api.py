from flask import Blueprint, request, make_response
from modules.utiles.create_response import create_response
from modules.sql_manager import SqlManager
from flask import jsonify

get_registrations_api_obj = Blueprint("get_registrations_api", __name__)

'''
GET REQUEST WITH PARAMETERS
event_id (query parameter)
auth_key (from cookies)
'''

@get_registrations_api_obj.route("/event/registrations/get", methods=["GET"])
def get_event_registrations():
    try:
        event_id = request.args.get("event_id")
        if not event_id:
            return {"message": "event_id is required", "code": 400}, 400
        
        try:
            event_id = int(event_id)
        except ValueError:
            return {"message": "event_id must be an integer", "code": 400}, 400
            
    except Exception as e:
        print("error occurred: ", e)
        return {"message": f"Invalid parameters: {e}", "code": 400}, 400

    try:
        with SqlManager().ClientEventHandler() as client_handler:
            result, code, message, registrations, event_name = client_handler.get_event_registrations(event_id)
        
        if result:
            response_data = {
                "code": code,
                "message": message,
                "event_name": event_name,
                "registrations": registrations,
                "data": registrations
            }
            return response_data, 200
        else:
            return {"message": f"{message}", "code": code}, code
    except Exception as e:
        print("error:", e)
        return {"message": f"Unknown error: {str(e)}", "code": 500}, 500
