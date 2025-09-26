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
            return "Successfully saved"
        except sqlite3.IntegrityError:
            return "Habit already exists"

    def load_habit(self, habit):
        res = self.cursor.execute("""
                            SELECT * FROM habits WHERE habit_name = ?
                            """, (habit,))
        answer = res.fetchone()
        return answer
    
    def delete_habit(self, habit):
        res = self.cursor.execute("""
                                 DELETE FROM habits WHERE habit_name = ? 
                                  """, (habit,))
        del_status = res.fetchone()
        rows = self.cursor.rowcount
        if rows > 0:
            return "Habit succesfully deleted"
        elif del_status == None:
            return "There is no such habit"
            
        
        