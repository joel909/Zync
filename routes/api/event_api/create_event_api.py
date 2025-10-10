from flask import Blueprint,render_template,request,make_response
from flask import Blueprint,render_template,request,make_response
from modules.utiles.create_response import create_response

from modules.sql_manager import SqlManager
from flask import jsonify,make_response

create_event_api_obj = Blueprint("create_event_api",__name__)

user_handler_object = SqlManager().UserHandler()
'''
POST REQUEST WITH PARAMETERS
core_events
event_name
description
ev_date
venue
auth_key
'''

@create_event_api_obj.route("/event/create",methods=["POST"])
def create_event():
    try:
        core_event = request.get_json()["type"]
        event_name = request.get_json()["name"]
        description = request.get_json()["description"]
        ev_date = request.get_json()["date"]
        venue = request.get_json()["venue"]
        auth_key = request.cookies.get("auth-key")
            # email_id = 
            # if(user_handler_object.get_email_id_with_auth_key(auth_key)[-1]):
    except Exception as e:
        if e=="description" or "core_events" or "event_name" or "ev_date" or "venue":
            print("error occured : ",e)
            return {"message":f"Invalid Fields Please Enter all fields correctly missing field is {e}","code":400},400
    try:
        with SqlManager().EventHandler() as event_handler_object:
            result,code,message = event_handler_object.create_new_event(core_event,event_name,description,ev_date,venue,auth_key)
        if result:
            response = create_response(message,code)
            print(response)
            return response
        else:
            return {"message":f"{message}","code":code},code
    except Exception as e:
        return {"message":f"Unknown error","code":500},500

