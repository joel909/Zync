from flask import Blueprint,request
from modules.sql_manager import SqlManager

non_auth_routes = ["/admin/login","/home","/admin/signup","/admin/api/signup","/favicon.ico"]
def authenticate_user():
    if request.path not in non_auth_routes:
        is_authenticated = False
        try:
            with SqlManager().UserHandler() as user_handler_object:
                auth_token = request.cookies.get("auth-key")
                if auth_token:
                    is_authenticated,status,message,email_id = user_handler_object.get_email_id_with_auth_key(auth_key=auth_token)
                    # print("running")
                    print("auth status",is_authenticated,"email",email_id)
                else:
                    is_authenticated = False
        except Exception as e:
            print("ERROR Occured",e)
            is_authenticated = False
        #print("the requested path is ",request.path)
        #print("use is ",is_authenticated)
        return is_authenticated
    else:
        return True

