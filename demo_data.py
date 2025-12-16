"""
Demo data for habit tracker application.
Provides 5 predefined habits with 4 weeks of realistic tracking data.
"""

from datetime import date, timedelta
from habits import Habit

today = date.today()

demo_habits = [
    Habit("Brush teeth", "daily", "Brush teeth twice daily"),
    Habit("Walk 10.000 steps", "daily", "Walk 10000 steps daily"),
    Habit("Exercise", "weekly", "Do some sport every week"),
    Habit("Clean room", "weekly", "I want to clean my room every week"),
    Habit("Go to cinema", "weekly", "I want to go to cinema once per week")
]

# region demo data
demo_tracking_data = {
    "Brush teeth" : [
        today, 
        today - timedelta(1),
        today - timedelta(2),
        today - timedelta(3),
        today - timedelta(4),
        today - timedelta(6),
        today - timedelta(7),
        today - timedelta(8),
        today - timedelta(9),
        today - timedelta(10),
        today - timedelta(11),
        today - timedelta(12),
        today - timedelta(13),
        today - timedelta(14),
        today - timedelta(16),
        today - timedelta(17),
        today - timedelta(18),
        today - timedelta(19),
        today - timedelta(20),
        today - timedelta(21),
        today - timedelta(22),
        today - timedelta(23),
        today - timedelta(25),
        today - timedelta(26)
    ],

    "Walk 10.000 steps" : [
        today,
        today - timedelta(1),
        today - timedelta(2),
        today - timedelta(4),
        today - timedelta(5),
        today - timedelta(6),
        today - timedelta(8),
        today - timedelta(10),
        today - timedelta(11),
        today - timedelta(12),
        today - timedelta(14),
        today - timedelta(15),
        today - timedelta(17),
        today - timedelta(19),
        today - timedelta(21),
        today - timedelta(23),
        today - timedelta(25),
        today - timedelta(26)
    ],

    "Go to cinema" : [
        today - timedelta(2),
        today - timedelta(11),
        today - timedelta(25)
    ],
    
    "Clean room" : [
        today - timedelta(3),
        today - timedelta(12),
        today - timedelta(26)
    ],

    "Exercise" : [
        today - timedelta(1),
        today - timedelta(8),
        today - timedelta(15),
        today - timedelta(22)
    ]
}

# endregion demo data


# region save data in storage 

def get_demo_habits():
    """Return list of predefined demo habits."""
    return demo_habits

def get_demo_tracking_data():
    """Return dict of demo tracking data."""
    return demo_tracking_data

def setup_demo_data(storage):
    """Load demo habits and tracking into storage."""

    # Save all demo habits
    for habit in get_demo_habits():
        storage.save_habit(habit)

    # Save all tracking data
    for habit_name, dates in get_demo_tracking_data().items():
        for date_entry in dates:
            tracking_data = (habit_name, date_entry)
            storage.save_tracking_data(tracking_data)

# endregion save data in storage