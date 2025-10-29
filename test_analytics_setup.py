import pytest
from freezegun import freeze_time
from datetime import datetime, date

from habits import Habit
from storage import SQLiteStorage
from test_database import db_setup, valid_habit

@pytest.fixture
def daily_habit():
    return Habit("10000 steps", "daily", "Walk 10000 steps per day")

@pytest.fixture
def weekly_habit():
    return Habit("go to Cinema", "weekly", "Watch a movie weekly")

@pytest.fixture
def single_entry_habit():
    return Habit("meditation", "weekly", "Meditate every day")

@pytest.fixture
def no_consecutive_dates_habit():
    return Habit("gym", "daily", "Want to go to gym everyday")

@pytest.fixture
def no_tracking_data_habit():
    return Habit("reading", "daily", "Want to read 10 Pages every day")

def test_multiple_habits(db_setup, valid_habit, daily_habit, weekly_habit):
    storage = SQLiteStorage(db_setup)
    storage.save_habit(valid_habit)
    storage.save_habit(daily_habit)
    storage.save_habit(weekly_habit)
    


@freeze_time("2025-09-29")
def test_today():
    assert datetime.now().date() == date(2025,9,29)

# region tracking_data
@pytest.fixture
def tracking_test_data():
    return {
        #=== 5 REQUIERED HABITS (as named in conception.pdf)===#
        "Brush teeth": [
            date(2025,9,27), 
            date(2025,9,26), 
            date(2025,9,25), 
            date(2025,9,24),
            date(2025,9,23), 
            date(2025,9,21), 
            date(2025,9,20), 
            date(2025,9,19), 
            date(2025,9,18), 
            date(2025,9,17), 
            date(2025,9,16), 
            date(2025,9,15),
            date(2025,9,14), 
            date(2025,9,13), 
            date(2025,9,11), 
            date(2025,9,10),
            date(2025,9,9), 
            date(2025,9,8), 
            date(2025,9,7), 
            date(2025,9,6),
            date(2025,9,5), 
            date(2025,9,4), 
            date(2025,9,2), 
            date(2025,9,1)
        ],

        "Walk 10.000 steps": [
            date(2025,9,27), 
            date(2025,9,26), 
            date(2025,9,25), 
            date(2025,9,23),
            date(2025,9,22), 
            date(2025,9,21), 
            date(2025,9,19), 
            date(2025,9,17),
            date(2025,9,16), 
            date(2025,9,15), 
            date(2025,9,13), 
            date(2025,9,12),
            date(2025,9,10), 
            date(2025,9,8), 
            date(2025,9,6), 
            date(2025,9,4),
            date(2025,9,2), 
            date(2025,9,1)

        ],
            
        "Go to cinema": [
            date(2025,9,25),
            date(2025,9,16),
            date(2025,9,2)
        ],

        "Clean room": [
            date(2025,9,24), 
            date(2025,9,15), 
            date(2025,9,1)
        ],

        "Exercise": [
            date(2025,9,26),
            date(2025,9,19),
            date(2025,9,12),
            date(2025,9,5)
        ],

        #===TEST-SPECIFIC HABIGS (for existing tests)===#
        "10000 steps": [
            date(2025,9,27), date(2025,9,26), date(2025,9,25),
            date(2025,9,23), date(2025,9,22), date(2025,9,21),
            date(2025,9,19), date(2025,9,15)
        ],
        "meditation": [
            date(2025,9,26)
        ],
        "gym": [
            date(2025,9,26), date(2025,9,20), date(2025,9,18), date(2025,9,10)
        ],

        "go to Cinema": [
            date(2025,9,25),
            date(2025,9,16),
            date(2025,9,2)
        ],
        # "reading" gets no tracking data = empty, handled by setup
    }
# endregion tracking_data

@pytest.fixture
def setup_analytics_data(db_setup, daily_habit, weekly_habit, single_entry_habit, no_tracking_data_habit, no_consecutive_dates_habit,
                         tracking_test_data):
    storage = SQLiteStorage(db_setup)
    storage.save_habit(weekly_habit)
    storage.save_habit(daily_habit)
    storage.save_habit(single_entry_habit)
    storage.save_habit(no_consecutive_dates_habit)
    storage.save_habit(no_tracking_data_habit)
    for habit_name, dates_list in tracking_test_data.items():
        for single_data in dates_list:
            result = (habit_name, single_data)
            storage.save_tracking_data(result)
    
    yield storage


def test_save_analytics(setup_analytics_data):
    result = ("10000 steps", "2025-8-31")
    data_set = setup_analytics_data.save_tracking_data(result)
    success, message = data_set
    assert message == "Successfully saved"

    result2 = (None, "2025-9-24")
    data_set2 = setup_analytics_data.save_tracking_data(result2)
    success, message = data_set2
    assert message == "Invalid habit name"

    result3 = ("sleeping", "2025-9-29")
    data_set3 = setup_analytics_data.save_tracking_data(result3)
    success, message = data_set3
    assert message == "Habit name was not found"

    result4 = (" ", "2025-9-25")
    data_set4 = setup_analytics_data.save_tracking_data(result4)
    success, message = data_set4
    assert message == "Invalid habit name"

    result5 = ("go to Cinema", "2025-9-20")
    data_set5 = setup_analytics_data.save_tracking_data(result5)
    success, message = data_set5
    assert message == "Successfully saved"


def test_load_analytics(setup_analytics_data):

    result = setup_analytics_data.load_tracking_data("10000 steps")

    assert result[0][0] == "2025-09-27"
    assert len(result) == 8

def test_delete_analytics(setup_analytics_data):
    result1 = ("10000 steps", "2025-09-23")
    data_set1 = setup_analytics_data.delete_tracking_data(result1)

    assert data_set1 == "Data successfully deleted"

    result2 = ("sleeping", "2025-09-20")
    data_set2 = setup_analytics_data.delete_tracking_data(result2)

    assert data_set2 == "Habit name was not found"

    result3 = ("10000 steps", "2025-09-29")
    data_set3 = setup_analytics_data.delete_tracking_data(result3)

    assert data_set3 == "No data found"

def test_load_all_habits(setup_analytics_data):
    habit_list = setup_analytics_data.load_all_habits()
    print(habit_list)
    for habit in habit_list:
        print(f'The Habit is {habit}')