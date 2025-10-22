# region imports
from test_analytics_setup import setup_analytics_data, freeze_time
from datetime import datetime, timedelta, date

# endregion

# region streaks

# region longest streak
def longest_streak(storage, habit):
    dates_count = 1
    longest_streak = 0
    result = storage.load_tracking_data(habit)
    if result == "Habit name was not found":
        return f"Habit {habit} was not found"
    periodicity = storage.load_habit(habit)
    periodicity = periodicity["habit_periodicity"]
    dates = list(map(lambda row: datetime.strptime(row[0], "%Y-%m-%d").date(), result))
    if not dates:
        return f"No tracking data found for Habit {habit}"
    sorted_dates = sorted(dates)
    for i in range(1, len(sorted_dates)):
        gap = (sorted_dates[i] - sorted_dates[i-1]).days
        if periodicity == "daily":
            if gap == 1:
                dates_count += 1
            elif gap > 1:
                longest_streak = max(longest_streak, dates_count)
                dates_count = 1
        elif periodicity == "weekly":
            if gap > 13:
                longest_streak = max(longest_streak, dates_count)
                dates_count = 1
            elif 13 >= gap >= 7:
                dates_count += 1
        elif periodicity == "monthly":
            if 31 >= gap >= 28:
                dates_count +=1
            elif gap > 31:
                longest_streak = max(longest_streak, dates_count)
                dates_count = 1
    if dates_count > longest_streak:
        longest_streak = max(longest_streak, dates_count)
    return f"The longest streak for Habit {habit} is {longest_streak} day{"s" if longest_streak != 1 else "" }"

# endregion longest streak

# region current streak

def check_gap(gap_value, periodicity, is_gap_to_today=False):
    if periodicity == "daily":
        if is_gap_to_today:
            return gap_value <= 1
        else:
            gap_rules = (1, 1)
    elif periodicity == "weekly":
        if is_gap_to_today:
            return 6 >= gap_value
        else:
            gap_rules = (7, 13)
    elif periodicity == "monthly":
        if is_gap_to_today:
            return 28 >= gap_value
        else:
            gap_rules = (28, 31)

    min_gap, max_gap = gap_rules
    return min_gap <= gap_value <= max_gap

def create_return(habit, current_streak, is_success=True):
    if is_success:
        return f"The current streak for Habit {habit} is {current_streak} day{"s" if current_streak != 1 else "" }"
    else:
        return f"Error! The current streak for Habit {habit} is {current_streak} day{"s" if current_streak != 1 else "" }"

def current_streak(storage, habit):
    current_streak = 0
    result = storage.load_tracking_data(habit)
    if result == "Habit name was not found":
        return f"Habit {habit} was not found"
    periodicity = storage.load_habit(habit)
    periodicity = periodicity["habit_periodicity"]
    dates = list(map(lambda row: datetime.strptime(row[0], "%Y-%m-%d").date(), result))
    if not dates:
        return f"No tracking data found for Habit {habit}"
    sorted_dates = sorted(dates)
    gap_to_today = (datetime.now().date() - sorted_dates[len(sorted_dates) - 1]).days
    if not check_gap(gap_to_today, periodicity, is_gap_to_today=True):
        return create_return(habit, current_streak, is_success=False)
    else:
        current_streak += 1
    if len(sorted_dates) > 1:
        for i in range(len(sorted_dates)-1, 0, -1):
            gap = (sorted_dates[i] - sorted_dates[i - 1]).days
            if check_gap(gap, periodicity):
                current_streak += 1
            else:
                return create_return(habit, current_streak)
    else:
        return create_return(habit, current_streak)

# endregion current streak

# region completion rate

def get_completion(periodicity):
    days = 30
    if periodicity == "daily":
        return days / 1
    elif periodicity == "weekly":
        return days // 7
    elif periodicity == "monthly":
        return days / 30

def completion_rate(storage, habit):
    completion_rate = 0
    today = datetime.now()
    time_span_dt = today - timedelta(days=30)
    time_span = time_span_dt.date()
    result = storage.load_tracking_data(habit)
    if result == "Habit name was not found":
        return f"Habit {habit} was not found"
    periodicity = storage.load_habit(habit)
    periodicity = periodicity["habit_periodicity"]
    expected_completions = get_completion(periodicity)
    dates = list(map(lambda row: datetime.strptime(row[0], "%Y-%m-%d").date(), result))
    time_span_result = list(filter(lambda x: time_span <= x <= today.date(), dates))
    completion_rate = (len(time_span_result) * 100) / expected_completions
    return f'Completion rate for the Habit {habit} is {completion_rate:.3g}%'

# endregion completion rate

# endregion