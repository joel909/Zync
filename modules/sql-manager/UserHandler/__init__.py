import mysql.connector
import string
import secrets

class ZyncApp:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='192.168.100.243',
            user='zync',
            password='123',
            database='zyncdb_'
        )
        self.cursor = self.conn.cursor()

    def generate_auth_key(self, length=20):
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

    def signup(self):
        name = input("Enter name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        auth_key = self.generate_auth_key()

        query = "INSERT INTO users (name, email, password, auth_key) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (name, email, password, auth_key))
        self.conn.commit()
        print("User inserted successfully with auth_key:", auth_key)

    

    def close(self):
        self.cursor.close()
        self.conn.close()