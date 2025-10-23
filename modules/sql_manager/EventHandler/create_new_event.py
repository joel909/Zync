def create_new_event(self, core_event, event_name, description, ev_date, venue, auth_key):
    try:
        # Use parameterized query to prevent SQL injection
        query = """
            INSERT INTO events (core_event, event_name, description, ev_date, venue, auth_key)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.cursor.execute(query, (core_event, event_name, description, ev_date, venue, auth_key))
        self.connection.commit()

        return True, 200, "Successfully created the event"

    except Exception as e:
        print("ERROR OCCURRED:", e)
        return False, 500, f"Failed to create event: {str(e)}"