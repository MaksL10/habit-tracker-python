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

def test_multiple_habits(db_setup, valid_habit, daily_habit, weekly_habit):
    storage = SQLiteStorage(db_setup)
    storage.save_habit(valid_habit)
    storage.save_habit(daily_habit)
    storage.save_habit(weekly_habit)


@freeze_time("2025-09-26")
def test_today():
    assert datetime.now().date() == date(2025,9,26)

@pytest.fixture
def tracking_test_data():
    return {
        "10000 steps": [
            date(2025,9,26),
            date(2025,9,25),
            date(2025,9,23),
            date(2025,9,22),
            date(2025,9,21),
            date(2025,9,19),
            date(2025,9,15)
        ],
            
        "go to Cinema": [
            date(2025,9,25),
            date(2025,9,16),
            date(2025,9,2)
        ]
    }

@pytest.fixture
def setup_analytics_data(db_setup,daily_habit, weekly_habit, tracking_test_data):
    storage = SQLiteStorage(db_setup)
    storage.save_habit(weekly_habit)
    storage.save_habit(daily_habit)
    for habit_name, dates_list in tracking_test_data.items():
        for single_data in dates_list:
            result = (habit_name, single_data)
            storage.save_tracking_data(result)
    
    yield storage


def test_save_analytics(setup_analytics_data):
    result = ("10000 steps", "2025-8-31")
    data_set = setup_analytics_data.save_tracking_data(result)
    assert data_set == "Successfully saved"

    result2 = (None, "2025-9-24")
    data_set2 = setup_analytics_data.save_tracking_data(result2)
    assert data_set2 == "Invalid habit name"

    result3 = ("sleeping", "2025-9-29")
    data_set3 = setup_analytics_data.save_tracking_data(result3)
    assert data_set3 == "Habit name was not found"

    result4 = (" ", "2025-9-25")
    data_set4 = setup_analytics_data.save_tracking_data(result4)
    assert data_set4 == "Invalid habit name"

    result5 = ("go to Cinema", "2025-9-20")
    data_set5 = setup_analytics_data.save_tracking_data(result5)
    assert data_set5 == "Successfully saved"


def test_load_analytics(setup_analytics_data):

    result = setup_analytics_data.load_tracking_data("10000 steps")

    assert result[0][0] == "2025-09-26"
    assert len(result) == 7

def test_delete_analytics(setup_analytics_data):
    result1 = ("10000 steps", "2025-09-23")
    data_set1 = setup_analytics_data.delete_tracking_data(result1)

    assert data_set1 == "Data succesfully deleted"

    result2 = ("sleeping", "2025-09-20")
    data_set2 = setup_analytics_data.delete_tracking_data(result2)

    assert data_set2 == "Habit was not found"

    result3 = ("10000 steps", "2025-09-27")
    data_set3 = setup_analytics_data.delete_tracking_data(result3)

    assert data_set3 == "No data found"
