import mysql.connector
from .UserHandler import Userhandler
from .EventHandler import EventHandler
class SqlManager:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host='169.254.196.213',user='zync',password='123')
            self.cursor = self.conn.cursor()
            self.cursor.execute("use zyncdb_users")
        except Exception as e:
            print("################### Database Connection FAILED ###############")
    def UserHandler(self):
        return Userhandler(self.conn,self.cursor)
    def EventHandler(self):
        return EventHandler(self.conn,self.cursor)

    

    def close(self):
        self.cursor.close()
        self.conn.close()