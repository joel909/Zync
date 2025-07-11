def sign_up(self,email,password,name,auth_key): 
    #query = f"insert into users values({name},{email},{password},{auth_key},null,null)"
    try:
        query = f'insert into users values("{name}","{email}","{password}","{auth_key}",null,null);'
        print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.commit()
        return True,200,"signup success",auth_key
    except Exception as e:
        print(e)
        return False,500,"signup failed",None
    
