from .create_new_event import create_new_event
from .get_all_events import get_all_events
class EventHandler():
    def __enter__(self):
        # setup code
        return self
    def __init__(self,connection,cursor):
        self.connection = connection
        self.cursor = cursor
    def create_new_event(self,core_event,event_name,description,ev_date,venue,auth_key):
        return create_new_event(self,core_event,event_name,description,ev_date,venue,auth_key)
    def get_all_events(self):
        return get_all_events(self=self)
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()


               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
            
               