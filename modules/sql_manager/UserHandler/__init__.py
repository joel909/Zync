import string
import secrets
from .sign_up import sign_up
class Userhandler():
    def __init__(self,connection,cursor):
        self.connection = connection
        self.cursor = cursor
    def sign_up(self,email,password,name):
        k =sign_up(self,email,password,name,"edfouw")
        return k
    def generate_auth_key(self, length=20):
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
            
               