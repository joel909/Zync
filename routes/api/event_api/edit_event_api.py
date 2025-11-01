from flask import Blueprint,render_template,request,make_response
from flask import Blueprint,render_template,request,make_response
from modules.utiles.create_response import create_response

from modules.sql_manager import SqlManager
from flask import jsonify,make_response

edit_event_api_obj = Blueprint("edit_event_api",__name__)

'''
POST REQUEST WITH PARAMETERS
event_id
core_event
event_name
description
ev_date
venue
auth_key
'''

@edit_event_api_obj.route("/event/edit",methods=["POST"])
def edit_event():
    try:
        event_id = request.get_json()["event_id"]
        core_event = request.get_json()["type"]
        event_name = request.get_json()["name"]
        description = request.get_json()["description"]
        ev_date = request.get_json()["date"]
        venue = request.get_json()["venue"]
        auth_key = request.cookies.get("auth-key")
    except Exception as e:
        print("error occured : ",e)
        return {"message":f"Invalid Fields Please Enter all fields correctly missing field is {e}","code":400},400
    try:
        with SqlManager().EventHandler() as event_handler_object:
            result,code,message = event_handler_object.edit_event(event_id,core_event,event_name,description,ev_date,venue,auth_key)
        if result:
            response = create_response(message,code)
            print(response)
            return response
        else:
            return {"message":f"{message}","code":code},code
    except Exception as e:
        return {"message":f"Unknown error","code":500},500
