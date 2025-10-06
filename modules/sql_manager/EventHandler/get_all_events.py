import datetime

def get_all_events(self):
    query = "SELECT * FROM events;"
    self.cursor.execute(query)
    result = self.cursor.fetchall()
    response_array = []
    print(result)
    for row in result:
        response = {"id":row[0],"name":row[2],"date":str(row[4]),"venue":row[5],"type":row[1],"description":row[3]}
        response_array.append(response)
    # print("the result obtained is : ",result)
    return response_array
