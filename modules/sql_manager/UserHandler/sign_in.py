def signin(self):
        email = input("Enter email: ")
        password = input("Enter password: ")

        query = "SELECT password, auth_key FROM users WHERE email = %s"
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()

        if result is None:
            print("Email not found. Please sign up first.")
            return None

        stored_password, auth_key = result
        if password == stored_password:
            print("Sign-in successful. Auth Key:", auth_key)
            return auth_key
        else:
            print("Incorrect password.")
            return None