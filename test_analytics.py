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