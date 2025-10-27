def sign_up(self, email, password, name, auth_key):
    try:
        # Use parameterized query to prevent SQL injection
        query = """
            INSERT INTO users (name, email, password, auth_key)
            VALUES (%s, %s, %s, %s);
        """
        self.cursor.execute(query, (name, email, password, auth_key))
        self.connection.commit()

        return True, 200, "Signup success", auth_key

    except Exception as e:
        print("ERROR OCCURRED:", e)
        return False, 500, "Signup failed", str(e)