def get_email_id_with_auth_key(self,auth_key):
    try:
        query = f'SELECT email FROM users WHERE auth_key = "{auth_key}";'
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print("requested user's email is ",result )  
        if result == []:
            raise Exception
        return True,200,"found email id",result
    except Exception as e:
        print("ERROR OCCURED",e)
        return False,500,"signup failed",e

