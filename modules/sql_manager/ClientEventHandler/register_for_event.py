
def register_for_event(self, event_id, name, school, dob, grade, contact):
    try:
        # Generate a unique registration ID

        # Insert registration record into the database
        insert_query = """
            INSERT INTO registrations (event_id, name, school, DOB, grade, contact_details)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.cursor.execute(insert_query, (event_id, name, school, dob, grade, contact))
        self.connection.commit()

        return True, 200, "Registration successful", {"event_id": event_id}

    except Exception as e:
        print("ERROR OCCURRED:", e)
        return False, 500, "Registration failed", str(e)