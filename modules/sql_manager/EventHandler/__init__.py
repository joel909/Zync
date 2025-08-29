import string
import secrets
from .create_new_event import create_new_event
class EventHandler():
    def __init__(self,connection,cursor):
        self.connection = connection
        self.cursor = cursor
    def create_new_event(self,core_event,event_name,description,ev_date,venue,auth_key):
        return create_new_event(self,core_event,event_name,description,ev_date,venue,auth_key)


               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
            
               