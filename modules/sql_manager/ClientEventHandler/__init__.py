from .register_for_event import register_for_event
from .get_event_registrations import get_event_registrations

class ClientEventHandler():
    def __enter__(self):
        # setup code
        return self
    def __init__(self,connection,cursor):
        self.connection = connection
        self.cursor = cursor
    def register_for_event(self,event_id,name,school,dob,grade,contact):
        return register_for_event(self,event_id,name,school,dob,grade,contact)
    def get_event_registrations(self, event_id):
        return get_event_registrations(self, event_id)
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
