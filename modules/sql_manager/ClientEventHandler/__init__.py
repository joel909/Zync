from .register_for_event import register_for_event
class ClientEventHandler():
    def __enter__(self):
        # setup code
        return self
    def __init__(self,connection,cursor):
        self.connection = connection
        self.cursor = cursor
    def register_for_event(self,event_id,name,school,dob,grade,contact):
        return register_for_event(self,event_id,name,school,dob,grade,contact)
        # Logic to register a user for an event
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
