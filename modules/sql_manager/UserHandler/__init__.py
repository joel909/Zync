import string
import secrets

from .get_email_id import get_email_id_with_auth_key
from .sign_up import sign_up
from .sign_in import signin
class Userhandler():
    def __init__(self,connection,cursor):
        self.connection = connection
        self.cursor = cursor
    def sign_in(self,email,password):
        return signin(self,email,password)
    def generate_auth_key(self, length=20):
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
    def get_email_id_with_auth_key(self,auth_key):
        return get_email_id_with_auth_key(self,auth_key=auth_key)
    def sign_up(self,email,password,name):
        k =sign_up(self,email,password,name,Userhandler.generate_auth_key(self))
        return k


               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
            
               