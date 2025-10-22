# region imports

import pytest
import questionary
from datetime import date

from test_analytics_setup import (
    setup_analytics_data, 
    daily_habit, 
    weekly_habit, 
    tracking_test_data, 
    single_entry_habit,
    no_consecutive_dates_habit,
    no_tracking_data_habit
)

from test_database import db_setup
from storage import SQLiteStorage
from analytics import longest_streak, current_streak, completion_rate
from habits import Habit
from main import setup_database, smart_start, create_completion, main_menu, show_analytics, create_habit, quit_app

# endregion imports

def test_questionary(setup_analytics_data):
    storage = setup_analytics_data

    habit_list = storage.load_all_habits()
    print(f'Verfügbare Habits sind: {habit_list}')

    if habit_list:
        selected = questionary.select(
            "Welches Habit tracken?",
            choices=habit_list
        ).ask()
        print(f"Gewählt: {selected}")
    else:
        print("Keine Habits!")

# region Habits and habit tracking data setup

def create_test_habits():
    """Returns list of test habits"""
    return [
        Habit("10000 steps", "daily", "Walk 10000 steps per day"),
        Habit("go to Cinema", "weekly", "Watch a movie weekly"), 
        Habit("meditation", "weekly", "Meditate every day"),
        Habit("gym", "daily", "Want to go to gym everyday"),
        Habit("reading", "daily", "Want to read 10 Pages every day")
    ]

def get_test_tracking_data():
    """Returns dict of test tracking data"""
    return {
        "10000 steps": [
            date(2025,9,27), date(2025,9,26), date(2025,9,25),
            date(2025,9,23), date(2025,9,22), date(2025,9,21),
            date(2025,9,19), date(2025,9,15)
        ],
        "go to Cinema": [date(2025,9,25), date(2025,9,16), date(2025,9,2)],
        "meditation": [date(2025,9,26)],
        "gym": [date(2025,9,26), date(2025,9,20), date(2025,9,18), date(2025,9,10)]
    }

def populate_test_data(storage):
    """Populate storage with test habits and tracking data"""
    # Save habits
    for habit in create_test_habits():
        result = storage.save_habit(habit)
    
    # Save tracking data  
    for habit_name, dates_list in get_test_tracking_data().items():
        for single_date in dates_list:
            result = (habit_name, single_date)
            storage.save_tracking_data(result)

# endregion habit and habit tracking data setup

def test_create_completion_success(setup_analytics_data):
    storage = setup_analytics_data
    
    success, message = create_completion(storage, "meditation")
    assert success == True
    assert message == "Successfully saved"

def test_create_completion_failure(setup_analytics_data):
    storage = setup_analytics_data

    success, message = create_completion(storage, "swimming")
    assert success == False
    assert message == "Habit name was not found"

def test_create_completion_no_habit(setup_analytics_data):
    storage = setup_analytics_data

    success, message = create_completion(storage, "")
    assert success == False
    assert message == "Invalid habit name"
    