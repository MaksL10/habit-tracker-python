# Habit Tracker Project
A Python CLI application for tracking personal habits and analyzing progress.

## What it does
- Track daily, weekly, and monthly habits  
- Calculate longest and current streaks
- Analyze completion rates over time
- Interactive command-line interface

## Requirements
- Python 3.7 or higher
- Git (for cloning the repository)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/[your-username]/habit-tracker-python.git
   cd habit-tracker-python
2. Create virtual environment:
    python -m venv habit-tracker-env

3. Activate virtual environment:
    # Windows (Git Bash)
    source habit-tracker-env/Scripts/activate

    # Windows (Command Prompt)
    habit-tracker-env\Scripts\activate

    # Linux/Mac
    source habit-tracker-env/bin/activate

4. Install dependencies:
    pip install -r requirements.txt
    ```

## Usage

### Starting the Application
```bash
python main.py
```

First Run

On first run, the application starts with an empty database. You can:

- Create your own habits using the menu system
- Follow the example habits from the project conception:
    - Brush teeth (daily)
    - Walk 10,000 steps (daily)
    - Exercise (weekly)
    - Clean room (weekly)
    - Go to cinema (weekly)

Note: Demo data with 4 weeks of tracking history is available in test fixtures for development/testing purposes.

Main Features
1. Create Your First Habit
    Main Menu → Create New Habit → Enter name, periodicity, description
2. Track Habit Completion
    Smart Start → Select habit (or Main Menu → Track Completion)
3. View Individual Habit Analytics
    Main Menu → Show analytics → Select habit

Example output:
Analytics for Walk 10,000 steps:
The longest streak for Habit Walk 10,000 steps is 4 days
The current streak for Habit Walk 10,000 steps is 2 days  
Completion rate for the Habit Walk 10,000 steps is 64%

4. Filter Habits by Type
    Main Menu → Show Habits by periodicity → Select daily/weekly/monthly
5. Create and Delete Habits
    Main Menu → Create New Habit → Enter details
    Main Menu → Delete Habit → Select habit to remove

### Running Tests

Make sure your virtual environment is activated, then run:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test files
pytest test_analytics_functions.py -v
pytest test_analytics_setup.py -v

# Run tests with coverage report
pytest --cov
```
Note: One interactive test (test_questionary) may fail in Git Bash due to terminal compatibility. 
Use Windows CMD for complete test suite, or run specific test files as shown above.

Test Structure

The test suite covers:

- Unit Tests: Individual function testing for all storage operations, analytics calculations, and habit validation
- Integration Tests: Complete workflow testing documented in integration_tests.md
- Edge Cases: Invalid inputs, empty databases, boundary values, and error scenarios
- Functional Programming: Testing of map(), filter(), and lambda implementations

Test Features

- Deterministic Testing: Uses freeze_time for consistent date-based testing
- Fixture-Based Setup: Comprehensive test data including 5 predefined habits with 4 weeks of tracking history
- Error Recovery: Validates graceful failure handling and user-friendly error messages
- Manual Integration: Documented user journey validation alongside automated tests

Expected Test Results

All tests should pass with output similar to:

test_analytics_functions.py::test_longest_streak PASSED
test_analytics_functions.py::test_current_streak PASSED
test_analytics_setup.py::test_setup_data PASSED

=================== 39 passed in 2.45s ===================

## Project Structure

habit-tracker-python/
│
├── main.py # Main application entry point
├── storage.py # Database operations and CRUD functionality
├── habits.py # Habit class with validation
├── analytics.py # Analytics functions using functional programming
├── habits.db # SQLite database (created on first run)
├── requirements.txt # Project dependencies
├── README.md # Project documentation
├── integration_tests.md # Manual integration test documentation
│
├── test_analytics_functions.py # Unit tests for analytics
├── test_analytics_setup.py # Test fixtures and setup
├── test_database.py # Database testing
├── test_main.py # CLI functionality tests
│
├── habit-tracker-env/ # Virtual environment
├── pycache/ # Python cache files
└── .pytest_cache/ # Pytest cache files


### Key Components

- **main.py**: CLI interface with questionary-based menus and user interaction flows
- **storage.py**: SQLiteStorage class handling all database operations with comprehensive error handling
- **habits.py**: Habit data model with property validation and input sanitization  
- **analytics.py**: Streak calculation and completion rate analysis using map(), filter(), and lambda functions
- **test_*.py**: Comprehensive test suite with fixtures, edge cases, and integration scenarios

## Technologies Used

### Core Technologies
- **Python 3.7+**: Modern Python features for object-oriented and functional programming
- **SQLite3**: Lightweight, serverless database for data persistence
- **pytest**: Industry-standard testing framework with fixtures and parametrization

### Libraries & Dependencies  
- **questionary**: Interactive command-line user interfaces and menu systems
- **freezegun**: Time mocking for deterministic date-based testing
- **datetime**: Date and time manipulation for habit tracking and analytics

### Development Practices
- **Object-Oriented Programming**: Clean class design with encapsulation and validation
- **Functional Programming**: Extensive use of map(), filter(), lambda functions for data processing
- **Test-Driven Development**: Comprehensive unit and integration testing approach
- **Git Version Control**: Professional development workflow with meaningful commits

### Design Patterns & Architecture
- **MVC-like Separation**: Clear boundaries between data (Storage), logic (Analytics), and interface (CLI)
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Error Handling**: Graceful failure recovery with user-friendly error messages
- **Documentation**: Professional docstrings and inline documentation throughout

## Contributing

This is an academic project developed for the course "Object-Oriented and Functional Programming in Python" (DLBDSOOFPP01) at IU International University.

### Academic Context
- **Course**: DLBDSOOFPP01 - Project: Object Oriented and Functional Programming in Python
- **Program**: Diploma Python and SQL Programming  
- **Institution**: IU International University
- **Submission**: Finalization Phase (Portfolio Part 3)

### Project Goals
This project demonstrates:
- Object-oriented design principles with Python classes and encapsulation
- Functional programming techniques using map(), filter(), and lambda functions
- Professional development practices including testing, documentation, and version control
- Database integration with SQLite for data persistence
- CLI application development with user-friendly interfaces

### Technical Journey
This project marked several important firsts:
- First large-scale Python application with virtual environments
- First object-oriented design implementation  
- Introduction to functional programming (map, filter, lambda)
- First comprehensive pytest testing suite
- First professional documentation and Git workflow

### Feedback Welcome
While this is submitted as coursework, constructive feedback on code structure, 
design patterns, or implementation approaches is welcome for educational purposes.

### Contact
For academic inquiries or technical discussions about this implementation:
- **Student**: Maksym Los
- **Student ID**: 10772973
- **GitHub**: MaksL10

