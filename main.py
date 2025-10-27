# region imports

import sqlite3
import questionary
from datetime import datetime

from storage import SQLiteStorage
from habits import Habit
from analytics import longest_streak, current_streak, completion_rate

# endregion imports

def setup_database():
    """
    Set up database connection and initialize schema.

    Creates connection to habits.db and creates 2 tables if they don't exist:
    - habits: Stores habit ID, name, periodicity, and description  
    - tracking: Stores tracking ID, habit ID, and completion dates

    Enables foreign key constraints for data integrity.

    Returns:
        sqlite3.Connection: Active database connection to habits.db.
    """
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits(
            habit_id INTEGER PRIMARY KEY,
            habit_name VARCHAR UNIQUE,
            habit_periodicity VARCHAR,
            habit_description VARCHAR) 
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracking(
            tracking_id INTEGER PRIMARY KEY,
            habit_id INTEGER,
            completion_date DATE,

            FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE)
    """)

    return conn

def main():
    """
    Main application entry point and event loop.
    
    Initializes database connection and enters interactive CLI loop.
    Handles user navigation between smart start menu and main menu,
    processing user choices until exit is selected.
    
    Flow:
        1. Set up database connection and tables
        2. Enter main interaction loop  
        3. Handle smart start menu → main menu navigation
        4. Process user actions (create, delete, track, analytics)
        5. Clean exit on user request
        
    Returns:
        None: Application terminates when user exits
    """
    conn = setup_database()
    storage = SQLiteStorage(conn)

    while True:
        choice = smart_start(storage)

        if choice == "Exit":
            quit_app(conn)
            break
        elif choice == "Main Menu":
            while True:
                menu_choice = main_menu(storage)
                if menu_choice == "Track Completion":
                    choice = smart_start(storage)
                    if choice == "Exit":
                        quit_app(conn)
                        return
                    success, message = create_completion(storage, choice)
                    print(message)
                elif menu_choice == "Show analytics":
                    analytics = show_analytics(storage)
                    if analytics:
                        habit, longest, current, completion = analytics
                        print(f'Analytics for {habit}:')
                        print(longest)
                        print(current)
                        print(completion)
                        print()
                    else:
                        continue
                elif menu_choice == "Create New Habit":
                    while True:
                        success, message = create_habit(storage)
                        print(message)
                        if success:
                            break
                        choices = ["Try again", "Go back to main manu"]
                        choice = questionary.select("What do you want to do?", choices=choices).ask()
                        if choice == "Go back to main manu":
                            break
                elif menu_choice == "Delete Habit":
                    while True:
                        success, message = delete_habit(storage)
                        print(message)
                        if success:
                            break
                        choices = ["Try again", "Go back to main manu"]
                        choice = questionary.select("What do you want to do?", choices=choices).ask()
                        if choice == "Go back to main manu":
                            break
                    else:
                        print(message)
                elif menu_choice == "Exit" or menu_choice is None:
                    quit_app(conn)
                    return
        else:
            success, message = create_completion(storage, choice)
            print(message)


def smart_start(storage):
    """
    Display smart start menu for quick habit selection or navigation.
    
    Gets list of available habits, adds Main Menu and exit options. Prompts user to make a choice.
    
    Args:
        storage (SQLiteStorage): Database storage object
        
    Returns:
        str: User's selected choice (habit name, "Main Menu", or "Exit")
    """
    habits = storage.load_all_habits()
    choices = habits + ["Main Menu", "Exit"]

    return questionary.select("What do you want to do?", choices=choices).ask()


def create_completion(storage, habit):
    """
    Handle new completion through CLI interface.
    
    Gets today's date and saves it together with habit name to database.
    
    Args:
        storage (SQLiteStorage): Database storage object
        habit (str): Name of a habit for completion
        
    Returns:
        tuple: (success: bool, message: str)
    """
    today = datetime.now().date()
    data = (habit, today)
    
    success, message = storage.save_tracking_data(data)
    return (success, message)


def main_menu(storage):
    """
    Display main menu with available actions.
    
    Prompts user to select next action in the app.

    Args:
        storage (SQLiteStorage): Database storage object (unused but maintained for API consistency)
    
    Returns:
        str: User's selected choice or "Exit" if cancelled
    """
    choices = [
        "Show analytics",
        "Create New Habit",
        "Delete Habit",
        "Track Completion",
        "Exit"
    ]
    menu_choice = questionary.select("Main Menu - What would you like to do?", choices=choices).ask()

    if menu_choice is None:
        return "Exit"
    
    return menu_choice


def show_analytics(storage):
    """
    Display analytics for selected habit.
    
    Shows longest streak, current streak, and completion rate for chosen habit.
    Calls all three analytics functions and displays results.
    
    Note:
        Known UX limitation: Habits without tracking data will show 
        duplicate "No tracking data found" messages from longest_streak() 
        and current_streak(), while completion_rate() shows 0%.
        
    Returns:
        tuple of False:
            - (habit_name, longest_streak_result, current_streak_result, completion_rate_result) if analytics generated
            - False if user cancels selection or goes back to main menu
    """
    habits = storage.load_all_habits()
    choices = habits + ["Go back to main Menu"]
    habit = questionary.select("Choose a habit for analytics: ", choices=choices).ask()

    if habit == "Go back to main Menu":
        return False
    
    longest = longest_streak(storage, habit)
    current = current_streak(storage, habit)
    completion = completion_rate(storage, habit)

    analytics_data = (habit, longest, current, completion)
    
    return analytics_data

def create_habit(storage):
    """
    Handle new habit creation through CLI interface.
    
    Prompts user for habit details, validates input, and saves to database.
    Includes error recovery workflow for invalid inputs.
    
    Args:
        storage (SQLiteStorage): Database storage object
        
    Returns:
        tuple: (success: bool, message: str)
    """

    name = questionary.text("Enter habit name:").ask()

    ## ====== DOUBLE VALIDATION SECTION ======##
    if not name or not name.strip():
        return False, "Error: Habit name cannot be empty"
    elif len(name.strip()) == 1:
        return False, "Error: Habit name is too short"
    elif len(name.strip()) > 20:
        return False, "Error: Habit name is too long"
    elif name.strip().isdigit():
        return False, "Error: Habit name cannot be a digit"
    elif name.strip() in ["daily", "weekly", "monthly"]:
        return False, "Error: Invalid habit name"
    
    periodicity = questionary.select("Select periodicity: ", choices=["daily", "weekly", "monthly"]).ask()
    description = questionary.text("Enter description (optional):").ask()

    try:
        habit = Habit(name, periodicity, description)
        result = storage.save_habit(habit)
        if result:
            return (True, "Habit successfully saved")
        else:
            return (False, "Habit already exists")
    except ValueError as e:
        return (False, f"Error: {e}")
    

def delete_habit(storage):
    """
    Handle deletion of existing habit through CLI interface.
    
    Prompts user to choose habit from list, validates selection, and performs the deletion from database.
    Includes error recovery workflow for invalid inputs.
    
    Args:
        storage (SQLiteStorage): Database storage object
        
    Returns:
        tuple: (success: bool, message: str)
    """

    choices = storage.load_all_habits()
    if not choices:
        return (False, "No habits to delete")
    
    habit = questionary.select("Choose a habit to delete: ", choices=choices).ask()
    if not habit:
        return (False, "Deletion canceled")

    success, message = storage.delete_habit(habit)
    
    return (success, message)


def quit_app(conn):
    """
    Quit the application gracefully.
    
    Displays goodbye message and closes database connection.

    Args:
        conn (sqlite3.connection): connection to SQLite3 Database.
    
    Returns:
        None: Function performs cleanup and exits
    """
    print("See you next time!")
    print("The app has been closed")
    conn.close()


if __name__ == "__main__":
    main()