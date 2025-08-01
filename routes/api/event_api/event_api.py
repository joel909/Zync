from flask import Blueprint,render_template,request,make_response
from flask import Blueprint,render_template,request,make_response
from modules.utiles.create_response import create_response

from modules.sql_manager import SqlManager
from flask import jsonify,make_response

create_event_api_obj = Blueprint("create_event_api",__name__)
event_handler_object = SqlManager().EventHandler()

@create_event_api_obj.route("/create/event",methods=["POST"])
def create_event():
    core_event = request.get_json()["core_events"]
    event_name = request.get_json()["event_name"]
    description = request.get_json()["description"]
    ev_date = request.get_json()["ev_date"]
    venue = request.get_json()["venue"]
    result,code,message = event_handler_object.create_new_event(core_event,event_name,description,ev_date,venue)
    if result:
        response = create_response(message,code)
        print(response)
        return response
    else:
        return {"message":f"{message}","code":code},code

