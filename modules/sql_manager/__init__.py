import mysql.connector
from .ClientEventHandler import ClientEventHandler
from .UserHandler import Userhandler
from .EventHandler import EventHandler
import os
from dotenv import load_dotenv
class SqlManager:
    def __init__(self):
        load_dotenv()
        # from .env: DB_HOST, DB_USER, PASSWORD (raw), DB_NAME
        host = os.getenv('DB_HOST') or os.getenv('HOST') or '169.254.196.213'
        user = os.getenv('DB_USER') or os.getenv('USER') or 'zync'
        DB_PASSWORD = os.getenv('DB_PASSWORD')  # use raw password field from .env
        database = os.getenv('DB_NAME') or os.getenv('DATABASE') or 'zyncdb_users'

        try:
            # print(f"connecting to database... with {host},{user},{database},{DB_PASSWORD}")
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=DB_PASSWORD,
                database=database,
                auth_plugin='mysql_native_password'
            )
            
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("################### Database Connection FAILED ###############")
            print(e)
            self.conn = None
            self.cursor = None
    def UserHandler(self):
        return Userhandler(self.conn,self.cursor)
    def EventHandler(self):
        #self.cursor = self.conn.cursor()
        return EventHandler(self.conn,self.cursor)
    def ClientEventHandler(self):
        return ClientEventHandler(self.conn,self.cursor)
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()
    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()