import sqlite3

# region SQLiteStorage class
class SQLiteStorage:

    """
    SQLite database storage handler for habit tracking system.
    
    Manages persistence of habits and tracking data using SQLite database.
    Provides CRUD operations with error handling and data validation.
    
    Attributes:
        connection: SQLite database connection object
        cursor: Database cursor for executing SQL commands
    """

    # region Initialisation
    def __init__(self, connection):
        """
        Initialize SQLiteStorage with database connection.
        
        Sets up row factory for dict-like access to query results and 
        creates cursor for database operations.
        
        Args:
            connection: sqlite3.Connection object to existing database
        """
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    # endregion Initialisation

    # region Habit operations
    def save_habit(self, habit):
        """
        Save a new habit to a database.

        Inserts habit data into habits table with duplicate name protection.
        Automaticly commits transaction on success.

        Args:
            habit (Habit): Habit object containing name, periodicity and description.

        Returns:
            bool: True if habit saved successfully, False if name already exists
            
        Raises:
            sqlite3.IntegrityError: If habit name violates UNIQUE constraint
        """
        try:
            self.cursor.execute("""
                    INSERT INTO habits (habit_name, habit_periodicity, habit_description) VALUES
                    (?, ?, ?)
                """, (habit.name, habit.periodicity, habit.description))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e: # <--- NEUER BLOCK: Fängt ALLE ANDEREN Fehler
            self.connection.rollback() # <--- WICHTIG: Stellt sicher, dass keine halben Daten drin bleiben
            raise e # <--- WIRF DEN FEHLER NEU, UM TRACEBACK ZU ERHALTEN!

    
    def load_habit(self, habit):
        """
        Load a single habit by name from database.

        Retrieves complete habit information including ID, name, periodicity 
        and description for the specified habit name

        Args:
            habit (str): Name of the habit to retrieve.

        Returns:
            sqlite3.Row: Habit data with dict-like access, or None if habit not found
        
        Example:
            habit_data = storage.load_habit("running")
            if habit_data:
                print(habit_data["habit_periodicity"])
        """
        res = self.cursor.execute("""
                            SELECT * FROM habits WHERE habit_name = ?
                            """, (habit,))
        answer = res.fetchone()
        return answer
    
    def load_all_habits(self):
        """
        Load all habits by name from database.

        Retrieves complete list of habit names for UI display
        and user selection in CLI menus.

        Returns:
            list: List of all habit names as strings, empty list if no habits exist.
        """
        res = self.cursor.execute("SELECT habit_name FROM habits")
        answer = res.fetchall()
        return [habit["habit_name"] for habit in answer]
    
    def delete_habit(self, habit):
        """
        Delete single habit by name from database.

        Delete complete habit information including ID, name, periodicity 
        and description for specified habit name. All tracking data will be also deleted on cascade
        from tracking table.

        Args:
            habit (str): Name of the habit to delete.

        Returns:
            tuple: (success: bool, message: str)

        Example:
            success, message = storage.delete_habit("running")
            if success:
                print(message)
            else:
                print(message)
        """
        res = self.cursor.execute("""
                                 DELETE FROM habits WHERE habit_name = ? 
                                  """, (habit,))
        self.connection.commit()
        if self.cursor.rowcount > 0:
            return (True, "Habit succesfully deleted")
        else:
            return (False, "There is no such habit")
    # endregion Habit operations

    # region Tracking Operations    
    def save_tracking_data(self, data):
        """
        Save tracking data in a database.

        Save tracking data for certain habit in database. Check if habit name is not empty and
        if habit is stored in database. Gets ID of the habit from habits and use ID to save 
        tracking data in tracking table. 

        Args:
            data (tuple): (habit_name: str, completion_date: date).
            - habit_name: Name of the habit to track
            - completion_date: Date when habit was completed

        Returns:
            tuple:(success: bool, message: str)

        Examples:
            # Success case - valid habit and date:
            from datetime import date
            success, message = storage.save_tracking_data(("running", date(2025, 10, 23)))
            if success:
                print(message)  # "Successfully saved"
    
            # Error case - empty habit name:
            success, message = storage.save_tracking_data(("", date(2025, 10, 23)))
            if not success:
                print(message)  # "Invalid habit name"
    
            # Error case - whitespace only habit name:
            success, message = storage.save_tracking_data(("   ", date(2025, 10, 23)))
            if not success:
                print(message)  # "Invalid habit name"
    
            # Error case - habit not in database:
            success, message = storage.save_tracking_data(("nonexistent", date(2025, 10, 23)))
            if not success:
                print(message)  # "Habit name was not found"
    
            # Typical CLI usage pattern:
            today = datetime.now().date()
            success, message = storage.save_tracking_data(("meditation", today))
            if success:
                print("Habit tracked successfully!")
            else:
                print(f"Error tracking habit: {message}")
        """
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
        """
        Retrieve tracking data for a given habit.

        Retrieve all tracking data from tracking table for a certain habit. Check if habit name is not empty and
        if habit is stored in database. Gets ID of the habit from habits and use ID to retrieve completion dates for the given ID.

        Args:
            habit (str): Name of the habit to retrieve tracking data.

        Returns:
            list or str:
                - List of sqlite3.Row objects with completion dates (success)
                - Empty list if habit exists but no tracking data  
                - "Invalid habit name" if name is empty/whitespace
                - "Habit name was not found" if habit doesn't exist in database
        
        Note:
            Designed for analytics consumption. Returns raw data on success,
            specific error strings for different failure modes.

        Examples:
            # Typical analytics usage pattern:
            result = storage.load_tracking_data("running") 
            if result == "Habit name was not found":
                return f"Habit running was not found"
            if result == "Invalid habit name":
                return "Invalid input"
    
            # Process data for analytics:
            dates = list(map(lambda row: datetime.strptime(row[0], "%Y-%m-%d").date(), result))
            if not dates:
                return "No tracking data found"
    
            # Error case - empty name:
            result = storage.load_tracking_data("")
            # Returns: "Invalid habit name"
    
            # Success case - empty tracking:
            result = storage.load_tracking_data("new_habit")  
            # Returns: []

        """
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
        """
        Delete certain tracking data for given habit.

        Delete current completion date for given habit. Check if habit name is not empty and
        if habit is stored in database. Gets ID of the habit from habits and use ID to delete 
        tracking data in tracking table for given completion date.

        Args:
            data (tuple): (habit_name: str, completion_date: date).
            - habit_name: Name of the habit to track
            - completion_date: Date when habit was completed

        Returns:
            str:
                - "Data successfully deleted" (success)
                - "No data found" if habit doesn't exist in database
                - "Invalid habit name" if name is empty/whitespace
                - "Habit name was not found" if habit doesn't exist in database

        Note:
            Currently not implemented in CLI interface. 
            Available for future functionality or direct API usage.
        """
        habit_name, completion_date = data[0], str(data[1])
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

        self.cursor.execute("""
                            DELETE FROM tracking WHERE habit_id = ?
                            AND completion_date = ?
                            """, (habit_id, completion_date,))
        self.connection.commit()
        rows = self.cursor.rowcount
        if rows > 0:
            return "Data successfully deleted"
        else:
            return "No data found"
        
    def load_all_habits_by_periodicity(self, periodicity):
        """
        Load all habits with the same periodicity from database.

        Retrieves complete list of habit names for a given periodicity
        for user selection in CLI menus.

        Args:
            periodicity (str): Periodicity to search in DB: "daily", "weekly" or "monthly"

        Returns:
            list: List of all habit names as strings, empty list if no habits exist
        """

        res = self.cursor.execute("""
                                    SELECT habit_name FROM habits 
                                    WHERE habit_periodicity = ?
                                   """, (periodicity,)
                               )
        answer = res.fetchall()
        
        return [habit["habit_name"] for habit in answer]
        
    # endregion Tracking Operations

# enrregion SQLiteStorage class