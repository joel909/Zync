def get_email_id_with_auth_key(self,auth_key):
    try:
        query = f'SELECT email FROM users WHERE  auth_key = "{auth_key}";'
        #print("requested user's email is ", )  
        self.cursor.fetchall
        result = self.cursor.fetchall()
        self.connection.commit()
        return True,200,"found email id",auth_key
    except Exception as e:
        print(e)
        return False,500,"signup failed",None

