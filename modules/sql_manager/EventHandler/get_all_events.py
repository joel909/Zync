import datetime

def get_all_events(self):
    try:
        query = "SELECT * FROM events;"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        response_array = []
        for row in result:
            response = {
                "id": row[0],
                "type": row[1],
                "name": row[2],
                "description": row[3],
                "date": str(row[4]),
                "venue": row[5]
            }
            response_array.append(response)

        return response_array

    except Exception as e:
        print("ERROR OCCURRED:", e)
        return []