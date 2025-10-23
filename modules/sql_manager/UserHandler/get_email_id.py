def get_email_id_with_auth_key(self, auth_key):
    try:
        # Use parameterized query to prevent SQL injection
        query = 'SELECT email FROM users WHERE auth_key = %s;'
        self.cursor.execute(query, (auth_key,))
        result = self.cursor.fetchall()

        print("Requested user's email is:", result)

        if not result:
            raise Exception("No user found")

        return True, 200, "Found email ID", result

    except Exception as e:
        print("ERROR OCCURRED:", e)
        return False, 500, "Signup failed", str(e)