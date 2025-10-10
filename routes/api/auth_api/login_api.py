from flask import Blueprint,render_template,request,make_response
from flask import Blueprint,render_template,request,make_response
from modules.utiles.create_response import create_response

from modules.sql_manager import SqlManager
from flask import jsonify,make_response

login_api_obj = Blueprint("login_api",__name__)


@login_api_obj.route("/login",methods=["POST"])
def login_api():
    user_handler_object = SqlManager().UserHandler()
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    result,code,message,auth_key = user_handler_object.sign_in(email,password)
    print("user login hahaha",email)
    response = create_response(message,code,auth_key)
    print(response)
    return response