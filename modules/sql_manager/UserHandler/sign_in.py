def signin(self, email, password):
    try:
        # Use parameterized query to prevent SQL injection
        query = "SELECT password, auth_key FROM users WHERE email = %s"
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()

        if result is None:
            print("Email not found. Please sign up first.")
            return False, 404, "Sign-in failed: User not found", None

        stored_password, auth_key = result

        # Compare passwords (consider hashing in production)
        if password == stored_password:
            print("Sign-in successful. Auth Key:", auth_key)
            return True, 200, "Sign-in success", auth_key
        else:
            print("Incorrect password.")
            return False, 401, "Sign-in failed: Incorrect password", None

    except Exception as e:
        print("ERROR OCCURRED:", e)
        return False, 500, "Sign-in failed: Unknown error", str(e)