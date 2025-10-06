def get_all_events(self):
    query = "SELECT * FROM events;"
    self.cursor.execute(query)
    result = self.cursor.fetchall()
    print("the result obtained is : ",result)
