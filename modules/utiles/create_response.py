from flask import jsonify
def create_response(message,code,data=None):
    return {"message":message,"code":code,"data":data},code