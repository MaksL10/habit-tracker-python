# region imports
import pytest
import sqlite3
import sys
import os

from habits import Habit
from storage import SQLiteStorage

# endregion

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# region Basic Database Tests
def test_database_concection():
    """Test ob wir eine in-memory Database erstellen können"""
    # Arrange & Act
    conn = sqlite3.connect(':memory:')
    
    # Assert
    assert conn is not None
    
    # Cleanup
    conn.close()

def test_create_habits_table():
    """Test ob wir die habits Tabelle erstellen können"""
    # Arrange
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Act
    cursor.execute('''
        CREATE TABLE habits (
            habit_id INTEGER PRIMARY KEY,
            habit_name VARCHAR UNIQUE NOT NULL,
            habit_periodicity VARCHAR NOT NULL CHECK (habit_periodicity IN ('daily', 'weekly')),
            habit_description VARCHAR,
            created_time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

# Assert - Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='habits'")
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == 'habits'
    
    # Cleanup
    conn.close()

# endregion

# region Fixtures
# Fixtures - here we set up test database for our test functions

@pytest.fixture
def db_setup():
    con = sqlite3.connect(':memory:') # database for fixture uses is created.
    cursor = con.cursor()

    # DB Set-Up
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

    # Database is ready and waiting for usage
    yield con

    # Close Database after the test
    con.close()

@pytest.fixture
def valid_habit():
    return Habit("running", "weekly", "I want to run 5km every week")

@pytest.fixture(params=[
    pytest.param(("", "daily", "description"),id="name_empty"), # Parameter 1 -> checking an Empty String for a name
    pytest.param(("sport", "yearly", "description"),id="invalid_periodicity"), # Parameter 2 -> checking wrong periodicity
    pytest.param(("weekly", "running", "this is a small description"),id="swapped_arghs"), # Parameter 3 -> checking periodicity instead of name
    pytest.param(("t", "monthly", "this is a small description"), id="name_short"), # Parameter 4 -> testing short name
    pytest.param(("abcdefghiklmnopqrstuvwxyz", "monthly", "this is a small description"),id="name_long"), # Parameter 5 -> testing long habit name
    pytest.param(("2325049", "monthly", "this is a small description"),id="name_digits"), # Parameter 6 -> testing digits as a name
    pytest.param((None, "monthly", "this is a small description"),id="name_none"), # Parameter 7 -> testing None
    pytest.param((" 12345 ", "monthly", "this is a small description"), id="whitespace_digits"), # Parameter 8 -> testing stripping
    ])
def invalid_habit(request):
    return request.param

# endregion

# region Fixture tests
def test_valid_habit_fixture(valid_habit):
    """Test ob das valid_habit fixture korrekt funktioniert"""
    # Test alle Attribute
    assert valid_habit.name == "running"
    assert valid_habit.periodicity == "weekly" 
    assert valid_habit.description == "I want to run 5km every week"
    
    # Test ob es ein Habit-Objekt ist
    assert isinstance(valid_habit, Habit)
    
    # Test __str__ method
    habit_str = str(valid_habit)
    assert "running" in habit_str
    assert "weekly" in habit_str

def test_invalid_habit_fixture(invalid_habit):
    """Testing corner cases to catch possible mistakes"""
    name, periodicity, description = invalid_habit
    with pytest.raises(ValueError):
        Habit(name, periodicity, description)
# endregion

# Tests with fixtures - testing functionality of database functions
def test_save(db_setup, valid_habit):
    storage = SQLiteStorage(db_setup)
    result = storage.save_habit(valid_habit)
    assert result == "Successfully saved"
    
    result2 = storage.save_habit(valid_habit)
    assert result2 == "Habit already exists"

def test_load(db_setup, valid_habit):
    storage = SQLiteStorage(db_setup)
    storage.save_habit(valid_habit)
    load_result = storage.load_habit("running")
    assert load_result["habit_name"] == "running"
    assert load_result[1] == "running"
    assert load_result["habit_periodicity"] == "weekly"

def test_delete(db_setup, valid_habit):
    storage = SQLiteStorage(db_setup)
    storage.save_habit(valid_habit)
    del_result = storage.delete_habit("testing")
    assert del_result == "There is no such habit"
    del_result2 = storage.delete_habit("running")
    assert del_result2 == "Habit succesfully deleted"

# endregion