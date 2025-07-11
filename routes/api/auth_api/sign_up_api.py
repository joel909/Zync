from flask import Blueprint,render_template,request,make_response
from modules.utiles.create_response import create_response

from modules.sql_manager import SqlManager
from flask import jsonify,make_response

signup_api_obj = Blueprint("signup_api",__name__)

user_handler_object = SqlManager().UserHandler()

@signup_api_obj.route("/signup",methods=["POST"])
def signup_api():
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    name = request.get_json()["name"]
    result,code,message,auth_key = user_handler_object.sign_up(email,password,name)
    response = create_response(message,code,auth_key)
    print(response)
    return response
