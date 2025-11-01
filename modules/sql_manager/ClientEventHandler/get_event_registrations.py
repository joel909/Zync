def get_event_registrations(self, event_id):
    """
    Fetch all registrations for a specific event
    
    Args:
        event_id: The ID of the event
        
    Returns:
        (bool, code, message, registrations_list, event_name)
        - bool: True if successful, False if error
        - code: HTTP status code (200 for success, 400/500 for errors)
        - message: Success or error message
        - registrations_list: List of registration dictionaries
        - event_name: Name of the event
    """
    try:
        # Verify event exists
        verify_query = "SELECT event_name FROM events WHERE id = %s"
        self.cursor.execute(verify_query, (event_id,))
        event_result = self.cursor.fetchone()
        
        if not event_result:
            return (False, 404, "Event not found", [], None)
        
        event_name = event_result[0]
        
        # Fetch all registrations for this event
        registrations_query = """
            SELECT id, event_id, name, school, DOB, grade, contact_details, registered_at
            FROM registrations
            WHERE event_id = %s
            ORDER BY registered_at DESC
        """
        
        self.cursor.execute(registrations_query, (event_id,))
        registrations = self.cursor.fetchall()
        
        # Convert to list of dictionaries for JSON serialization
        registrations_list = []
        for reg in registrations:
            reg_dict = {
                'id': reg[0],
                'event_id': reg[1],
                'name': reg[2],
                'school': reg[3],
                'DOB': reg[4],
                'grade': reg[5],
                'contact_details': reg[6],
                'registered_at': str(reg[7]) if reg[7] else None
            }
            registrations_list.append(reg_dict)
        
        return (True, 200, f"Found {len(registrations_list)} registrations", registrations_list, event_name)
        
    except Exception as e:
        return (False, 500, f"Error fetching registrations: {str(e)}", [], None)
