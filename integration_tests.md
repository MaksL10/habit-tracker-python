# CLI Integration Tests - Habit Tracker

## Test Setup
- Delete `habits.db` file before testing
- Run `python main.py`

## Test Cases

### TC1: Fresh User - Create First Habit
- [x] No habits.db exists
- [x] Start app → Smart Start shows "Main Menu" and "Exit" only
- [x] Main Menu → Create New Habit
- [x] Enter valid habit data
- [x] Success message appears
- [x] Back to Smart Start → new habit appears in list

### TC2: Track Completion
- [x] Select habit from Smart Start
- [x] Success message displays
- [x] [Exit - App will be closed with 2 Messages]

### TC3: Delete Habit
- [x] start app -> Main Menu
- [x] Main Menu -> Delete Habit
- [x] Choose a Habit to Delete from a List
- [x] Choose valid Habit
- [x] Success Message appears
- [x] Back to Main Menu
- [x] Select Track Completion
- [x] Deleted Habit is not on the list

TC4: Error Recovery & Validation

[x] Create Habit mit leerem Namen → Error message
[x] "Try again" wählen → success
[x] Create duplicate Habit → "already exists" message
[x] Analytics for Habit without Tracking data → appropriate message

TC5: Multi-Habit User Journey

[x] Create 3 habits (daily, weekly, monthly)
[x] Track completion für alle 3
[x] Analytics für jeden - verify different calculations
[x] Delete one habit - verify others unaffected
[x] Track completion für remaining habits

TC6: Exit & Navigation Flow

[x] Exit from Smart Start → clean shutdown
[x] Exit from Main Menu → clean shutdown
[x] Main Menu → Track Completion → Exit (dein previous bug)
[x] ESC/Cancel in questionary prompts → graceful handling
[x] Multiple back-and-forth between Smart Start ↔ Main Menu

## Test Results
**Date:** [2025-10-21, 2025-10-22]
**Results:** All tests passed
**Issues:** [notes]