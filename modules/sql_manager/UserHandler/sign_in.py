def signin(self,email,password):
        try:
            query = "SELECT password, auth_key FROM users WHERE email = %s"
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()

            if result is None:
                print("Email not found. Please sign up first.")
                return False,500,"signup failed: User not found",None

            stored_password, auth_key = result
            if password == stored_password:
                print("Sign-in successful. Auth Key:", auth_key)
                return True,200,"signip success",auth_key
            else:
                print("Incorrect password.")
                return False,500,"signup failed: Incorrect Password",None
        except Exception as e:
             return False,500,"signup failed: Unknown Error",None