def create_new_event(self,core_event,event_name,description,ev_date,venue,auth_key):
    try:
        query = f'insert into events(core_event, event_name, description, ev_date, venue, auth_key) values("{core_event}","{event_name}","{description}","{ev_date}","{venue}","{auth_key}")'
        self.cursor.execute(query)
        self.connection.commit()
        return True,200,"successfully created the event"
    except Exception as e:
        print(e)
        return False,500,f"failed to create event cuz {e}"

        