import sqlite3

class SQLiteStorage:
    def __init__(self, connection):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def save_habit(self, habit):
        try:
            self.cursor.execute("""
                    INSERT INTO habits (habit_name, habit_periodicity, habit_description) VALUES
                    (?, ?, ?)
                """, (habit.name, habit.periodicity, habit.description))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    
    def load_habit(self, habit):
        res = self.cursor.execute("""
                            SELECT * FROM habits WHERE habit_name = ?
                            """, (habit,))
        answer = res.fetchone()
        return answer
    
    def load_all_habits(self):
        res = self.cursor.execute("SELECT habit_name FROM habits")
        answer = res.fetchall()
        return [habit["habit_name"] for habit in answer]
    
    def delete_habit(self, habit):
        res = self.cursor.execute("""
                                 DELETE FROM habits WHERE habit_name = ? 
                                  """, (habit,))
        self.connection.commit()
        if self.cursor.rowcount > 0:
            return (True, "Habit succesfully deleted")
        else:
            return (False, "There is no such habit")
    
    def save_tracking_data(self, data):
        habit_name, single_date = data[0], str(data[1])
        if not habit_name or not habit_name.strip():
            return (False, "Invalid habit name")
        
        res = self.cursor.execute("""
            SELECT habit_id FROM habits
            WHERE habit_name = ?
            """, (habit_name,))
        habit_id = res.fetchone()
        if not habit_id:
            return (False, "Habit name was not found")
        habit_id = habit_id["habit_id"]
                                          
        self.cursor.execute("""
            INSERT INTO tracking (habit_id, completion_date) 
            VALUES (?, ?)
            """, (habit_id, single_date))
        self.connection.commit()
        return (True, "Successfully saved")
    
    def load_tracking_data(self, habit_name):
        if not habit_name or not habit_name.strip():
            return "Invalid habit name"
        res = self.cursor.execute("""
            SELECT habit_id FROM habits
            WHERE habit_name = ?
            """, (habit_name,))
        habit_id = res.fetchone()
        if not habit_id:
            return "Habit name was not found"
        habit_id = habit_id["habit_id"]
        
        res = self.cursor.execute("""
                            SELECT completion_date FROM tracking WHERE habit_id = ?
                            """, (habit_id,))
        load_result = res.fetchall()
        return load_result
    
    def delete_tracking_data(self,data):
        habit_name, completion_date = data[0], str(data[1])
        if not habit_name or not habit_name.strip():
            return "Invalid habit name"
        res = self.cursor.execute("""
            SELECT habit_id FROM habits
            WHERE habit_name = ?
            """, (habit_name,))
        habit_id = res.fetchone()
        if not habit_id:
            return "Habit was not found"
        habit_id = habit_id["habit_id"]

        self.cursor.execute("""
                            DELETE FROM tracking WHERE habit_id = ?
                            AND completion_date = ?
                            """, (habit_id, completion_date,))
        rows = self.cursor.rowcount
        if rows > 0:
            return "Data succesfully deleted"
        else:
            return "No data found"