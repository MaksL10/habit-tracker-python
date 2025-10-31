# region imports
from test_analytics_setup import setup_analytics_data, freeze_time
from datetime import datetime, timedelta, date

# endregion

# region streaks

# region longest streak
def longest_streak(storage, habit):
    """
    Calculates the longest streak for a given habit.

    Called by the CLI to calculate the longest streak for a given habit.
    Retrieves all completion dates for that habit and validates habit existence.
    Obtains habit periodicity from habits table, as this is essential for calculating streaks.

    Analyzes tracking history using forward chronological iteration to detect 
    consecutive completion patterns. Applies periodicity-specific gap rules:
    daily (1 day), weekly (7-13 days), monthly (28-31 days).

    Args:
        storage (SQLiteStorage): Database storage object for accessing habit and tracking data
        habit (str): Name of the habit for analytics

    Returns:
            str:
                - "The longest streak for Habit {habit} is {longest_streak} day{"s" if longest_streak != 1 else ""}" (success)
                - "No tracking data found for Habit {habit}" if habit doesn't have any completion dates.
                - "Habit {habit} was not found" if habit doesn't exist in database

    """
    dates_count = 1
    longest_streak = 0
    result = storage.load_tracking_data(habit)
    if result == "Habit name was not found":
        return f"Habit {habit} was not found"
    habit_data = storage.load_habit(habit)
    periodicity = habit_data["habit_periodicity"]

    # Convert Row objects to date objects for arithmetic
    dates = list(map(lambda row: datetime.strptime(row[0], "%Y-%m-%d").date(), result))
    if not dates:
        return f"No tracking data found for Habit {habit}"
    
    # Sort chronologically (oldest to newest)
    sorted_dates = sorted(dates)
    for i in range(1, len(sorted_dates)):
        
        # Calculate days between consecutive completions
        gap = (sorted_dates[i] - sorted_dates[i-1]).days

        # Apply periodicity-specific gap rules to detect consecutive patterns
        # - Daily: exactly 1 day gap = consecutive
        # - Weekly: 7-13 day gap = consecutive  
        # - Monthly: 28-31 day gap = consecutive
        # Streak breaks when gaps exceed allowed range

        if periodicity == "daily":
            if gap == 1:
                dates_count += 1
            elif gap > 1:
                # Gap too large - streak broken, save current streak
                longest_streak = max(longest_streak, dates_count)
                dates_count = 1 # Reset counter
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
    # Final comparison needed - handles case where data ends with active streak
    if dates_count > longest_streak:
        longest_streak = max(longest_streak, dates_count)
    return f"The longest streak for Habit {habit} is {longest_streak} day{"s" if longest_streak != 1 else "" }"

# endregion longest streak

# region current streak

def check_gap(gap_value, periodicity, is_gap_to_today=False):
    """
    Validate if gap between dates is acceptable for given periodicity.
    
    Applies different rules for gap-to-today vs historical gaps.
    
    Args:
        gap_value (int): Number of days between dates
        periodicity (str): "daily", "weekly", or "monthly"
        is_gap_to_today (bool): Whether gap is from today or between completions
        
    Returns:
        bool: True if gap is valid for streak continuation, False otherwise
    """
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
    """
    Create return messages for current streak.

    Args:
        - habit (str): Habit name
        - current_streak (int): Count of current streak
        - is_success (bool): Whether given habit has a current streak or not

    Returns:
        str: Formatted message string
            -  "The current streak for Habit {habit} is {current_streak} day(s)" (success)
            - "Error! The current streak for Habit {habit} is {current_streak} day(s)" (no streak)
    """
    if is_success:
        return f"The current streak for Habit {habit} is {current_streak} day{"s" if current_streak != 1 else "" }"
    else:
        return f"Error! The current streak for Habit {habit} is {current_streak} day{"s" if current_streak != 1 else "" }"

def current_streak(storage, habit):
    """
    Calculates the current streak for a given habit.

    Called by the CLI to calculate the current streak for a given habit.
    Retrieves all completion dates for that habit and validates habit existence.
    Obtains habit periodicity from habits table, as this is essential for calculating streaks.

    Analyzes tracking history using backward chronological iteration from most recent completion 
    to detect consecutive completion patterns from today. Applies periodicity-specific gap rules:
    daily (1 day), weekly (7-13 days), monthly (28-31 days).

    Args:
        storage (SQLiteStorage): Database storage object for accessing habit and tracking data
        habit (str): Name of the habit for analytics

    Returns:
            str:
                - "The current streak for Habit {habit} is {current_streak} day{"s" if current_streak != 1 else "" }" (success)
                - "Error! The current streak for Habit {habit} is {current_streak} day{"s" if current_streak != 1 else "" }" 
                if gap from today exceeds periodicity limits
                - "No tracking data found for Habit {habit}" if habit doesn't have any completion dates.
                - "Habit {habit} was not found" if habit doesn't exist in database

    """
    current_streak = 0
    result = storage.load_tracking_data(habit)
    if result == "Habit name was not found":
        return f"Habit {habit} was not found"
    periodicity = storage.load_habit(habit)
    periodicity = periodicity["habit_periodicity"]
    # Convert Row objects to date objects for arithmetic
    dates = list(map(lambda row: datetime.strptime(row[0], "%Y-%m-%d").date(), result))
    if not dates:
        return f"No tracking data found for Habit {habit}"
    sorted_dates = sorted(dates)
    # Calculate gap between today and the latest completion date
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
    """
    Calculate expected number of completions in 30-day window for given periodicity.

    Args:
        periodicity (str): Periodicity for a habit
    
    Returns:
        int: Expected number of completions in 30 days
        - 30 for daily habits
        - 4 for weekly habits  
        - 1 for monthly habits
    """
    days = 30
    if periodicity == "daily":
        return days / 1
    elif periodicity == "weekly":
        return days // 7
    elif periodicity == "monthly":
        return days / 30

def completion_rate(storage, habit):
    """
    Calculate completion rate for a given habit.

    Called by the CLI to calculate the completion rate for a given habit.
    Calculate 30 days time span from today backwards. Retrieves all completion dates for that habit 
    and validates habit existence. Obtains habit periodicity from habits table, 
    as this determines expected completion frequency within the time window.

    Compares actual completions within 30-day window against expected completions based on periodicity. 
    Calculates percentage rate with smart formatting. 
    Expected completions in 30-day window:
    daily (30 completions), weekly (4 completions), monthly (1 completion).

    Args:
        storage (SQLiteStorage): Database storage object for accessing habit and tracking data
        habit (str): Name of the habit for analytics

    Returns:
            str:
                - 'Completion rate for the Habit {habit} is {completion_rate:.3g}%' (success)
                - "Habit {habit} was not found" if habit doesn't exist in database.
    """
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

# region longest streak by periodicity

def extract_streak_number(result):
    # "The longest streak for Habit X is 15 days"
    words = result.split()
    # Find "is" and take next word
    for i, word in enumerate(words):
        if word == "is":
            return int(words[i+1])

def longest_streak_by_periodicity(storage):
    """
    Find longest streaks grouped by periodicity.
    
    Returns longest streak for each periodicity type separately,
    allowing meaningful comparisons within same frequency.
    
    Returns:
        dict: {
            "daily": ("habit_name", streak_count),
            "weekly": ("habit_name", streak_count), 
            "monthly": ("habit_name", streak_count)
        }
    """
    results = []
    
    for periodicity in ["daily", "weekly", "monthly"]:
        habits = storage.load_all_habits_by_periodicity(periodicity)
        
        if not habits:
            results.append(f'No {periodicity} habits found')
        else: 
            best_habit = None
            best_streak = 0
            
            for habit in habits:
                streak_result = longest_streak(storage, habit)
                # Extract streak number from "The longest streak for Habit X is Y days"
                streak_count = extract_streak_number(streak_result)
                if not streak_count:
                    break
                
                if streak_count > best_streak:
                    best_streak = streak_count
                    best_habit = habit
            
            results.append(f'Best {periodicity.capitalize()} Habit: {best_habit} with {best_streak} streak')
    
    return "\n".join(results)
# endregion longest streak by periodicity
# endregion