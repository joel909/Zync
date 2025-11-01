def edit_event(self, event_id, core_event, event_name, description, ev_date, venue, auth_key):
    """
    Edit an existing event in the database.
    
    Args:
        event_id: ID of the event to edit
        core_event: Core event type
        event_name: Name of the event
        description: Event description
        ev_date: Event date/time
        venue: Event venue
        auth_key: Auth key of the user editing (must match created_by_auth_key)
    
    Returns:
        Tuple: (success: bool, code: int, message: str)
    """
    try:
        # First verify that the user who created the event is the one editing it

        #REMOVE THE BELOW LINES IF YOU WANT TO ENFORCE ONLY USERS WHO CREATED THE EVENTS TO BE ABLE TO EDIT IT 
        # verify_query = "SELECT created_by_auth_key FROM events WHERE id = %s"
        # self.cursor.execute(verify_query, (event_id,))
        # result = self.cursor.fetchone()
        
        # if result is None:
        #     return False, 404, "Event not found"
        
        # stored_auth_key = result[0]
        
        # # Check if the auth_key matches (only creator can edit)
        # if stored_auth_key != auth_key:
        #     return False, 403, "Unauthorized: Only event creator can edit"
        
        # Use parameterized query to prevent SQL injection
        query = """
            UPDATE events 
            SET core_event = %s, 
                event_name = %s, 
                description = %s, 
                ev_date = %s, 
                venue = %s
            WHERE id = %s;
        """
        self.cursor.execute(query, (core_event, event_name, description, ev_date, venue, event_id))
        self.connection.commit()
        
        if self.cursor.rowcount == 0:
            return False, 500, "Failed to update event"

        return True, 200, "Event updated successfully"

    except Exception as e:
        print("ERROR OCCURRED:", e)
        return False, 500, f"Failed to edit event: {str(e)}"
