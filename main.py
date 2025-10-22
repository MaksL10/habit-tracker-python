# import region

import sqlite3
import questionary
from datetime import datetime

from storage import SQLiteStorage
from habits import Habit
from analytics import longest_streak, current_streak, completion_rate

# end import region

def setup_database():
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
    habits = storage.load_all_habits()
    choices = habits + ["Main Menu", "Exit"]

    return questionary.select("What do you want to do?", choices=choices).ask()


def create_completion(storage, habit):
    today = datetime.now().date()
    data = (habit, today)
    
    result = storage.save_tracking_data(data)
    success, message = result
    return (success, message)


def main_menu(storage):
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
    choices = storage.load_all_habits()
    if not choices:
        return (False, "No habits to delete")
    
    habit = questionary.select("Choose a habit to delete: ", choices=choices).ask()
    if not habit:
        return (False, "Deletion canceled")

    success, message = storage.delete_habit(habit)
    
    return (success, message)


def quit_app(conn):
    print("See you next time!")
    print("The app has been closed")
    conn.close()


if __name__ == "__main__":
    main()