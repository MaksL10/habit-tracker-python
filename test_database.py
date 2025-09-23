import pytest
import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# Fixtures - here we set up test database for our test functions

@pytest.fixture
def db_setup():
    db = sqlite3.connect(':memory:') # database for fixture uses is created.
    cursor = con.cursor()

    # DB Set-Up
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits(
            habit_id INTEGER PRIMARY KEY,
            habit_name VARCHAR,
            habit_periodicity VARCHAR,
            habit_description VARCHAR) 
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracking(
            tracking_id INTEGER PRIMARY KEY,
            habit_id INTEGER,
            completion_date DATE,

            FOREIGN KEY (habit_id) REFERENCES habits(habit_id))
    """)

    # Database is ready and waiting for usage
    yield con

    # Close Database after the test
    con.close()

@pytest.fixture
def test_habit():
    # code

@pytest.fixture
def test_tracking():
    #code

# Tests with fixtures - testing functionality of database functions

def test_save():
    # code

def test_load():
    #code

def test_delete():
    #code