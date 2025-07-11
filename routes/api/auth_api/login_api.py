from flask import Blueprint,render_template,request,make_response

login_api_obj = Blueprint("login_api",__name__)

@login_api_obj.route("/login",methods=["POST"])
def login_api():
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    print("user login hahaha",email)
    response = make_response({"status":200,"message":"user authenticated"},200)
    response.set_cookie("auth-key","place-holder",max_age=60*60*24*30)
    return response