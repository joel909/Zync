def get_user_events(self,auth_key):
            query = f'select * from events where auth_key = "{auth_key}";'
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
