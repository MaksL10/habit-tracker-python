# region imports
import pytest
from datetime import datetime, date

from freezegun import freeze_time

from test_database import db_setup
from test_analytics_setup import (
    setup_analytics_data, 
    daily_habit, 
    weekly_habit, 
    tracking_test_data, 
    single_entry_habit,
    no_consecutive_dates_habit,
    no_tracking_data_habit
)

from analytics import longest_streak, current_streak, completion_rate

# endregion

# region test Streaks

# region test longest streak
def test_longest_streak(setup_analytics_data):
    result = longest_streak(setup_analytics_data, "10000 steps")
    assert result == f'The longest streak for Habit 10000 steps is 3 days'

def test_longest_streak_invalid_habit(setup_analytics_data):
    result = longest_streak(setup_analytics_data, "sleeping")
    assert result == f'Habit sleeping was not found'

def test_single_entry(setup_analytics_data):
    result = longest_streak(setup_analytics_data, "meditation")
    assert result == f'The longest streak for Habit meditation is 1 day'

def test_no_consecutive_dates(setup_analytics_data):
    result = longest_streak(setup_analytics_data, "gym")
    assert result == f'The longest streak for Habit gym is 1 day'

def test_no_tracking_data(setup_analytics_data):
    result = longest_streak(setup_analytics_data, "reading")
    assert result == f'No tracking data found for Habit reading'

# endregion test longest streak

# region test current streak
@freeze_time("2025-09-28")
def test_current_daily_streak(setup_analytics_data):
    result = current_streak(setup_analytics_data, "10000 steps")
    assert result == "The current streak for Habit 10000 steps is 3 days"

@freeze_time("2025-09-29")
def test_current_daily_streak_interrupted(setup_analytics_data):
    result = current_streak(setup_analytics_data, "10000 steps")
    assert result == "Error! The current streak for Habit 10000 steps is 0 days"

@freeze_time("2025-09-28")
def test_current_weekly_streak(setup_analytics_data):
    result = current_streak(setup_analytics_data, "go to Cinema")
    assert result == "The current streak for Habit go to Cinema is 2 days"

@freeze_time("2025-10-7")
def test_current_weekly_streak_interrupted(setup_analytics_data):
    result = current_streak(setup_analytics_data, "go to Cinema")
    assert result == "Error! The current streak for Habit go to Cinema is 0 days"

@freeze_time("2025-09-27")
def test_single_entry(setup_analytics_data):
    result = current_streak(setup_analytics_data, "meditation")
    assert result == 'The current streak for Habit meditation is 1 day'

def test_current_streak_no_habit(setup_analytics_data):
    result = current_streak(setup_analytics_data, "sleeping")
    assert result == "Habit sleeping was not found"

def test_current_streak_no_tracking_data(setup_analytics_data):
    result = current_streak(setup_analytics_data, "reading")
    assert result == "No tracking data found for Habit reading"

# endregion

# region test completion rate

@freeze_time("2025, 9, 21")
def test_completion_rate(setup_analytics_data):
    result = completion_rate(setup_analytics_data, "10000 steps")
    assert result == 'Completion rate for the Habit 10000 steps is 10%'

@freeze_time("2025, 10, 20")
def test_completion_rate_far_future(setup_analytics_data):
    result= completion_rate(setup_analytics_data, "10000 steps")
    assert result == 'Completion rate for the Habit 10000 steps is 20%'

@freeze_time("2025, 9, 15")
def test_completion_rate_low_completion(setup_analytics_data):
    result = completion_rate(setup_analytics_data, "10000 steps")
    assert result == 'Completion rate for the Habit 10000 steps is 3.33%'

@freeze_time("2025, 9, 30")
def test_completion_date_weekly(setup_analytics_data):
    result = completion_rate(setup_analytics_data, "go to Cinema")
    assert result == 'Completion rate for the Habit go to Cinema is 75%'


# endregion test completion rate