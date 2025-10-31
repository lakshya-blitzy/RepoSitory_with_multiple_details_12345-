# Calendar Step Definitions API Reference

## Overview

The Calendar step definitions module provides comprehensive Behave step implementations for testing calendar and meeting management workflows in the Testinium ERP application. This module supports calendar navigation, view switching (day/week/month), dynamic date validation, and complete meeting lifecycle operations (create, view, edit, save).

**Module:** `features/steps/calendar_steps.py`

**Source:** `features/steps/calendar_steps.py:1-656`

**Migration Context:**
- **Java Source:** `src/main/java/com/testinium/step_definitions/Calendar.java`
- **Pattern:** Cucumber `@When/@Then/@And` → Behave `@when/@then/@step`
- **Driver Access:** Static `Driver.getDriver()` → `context.driver` pattern

### Key Features

- **Calendar Navigation:** Navigate to calendar module from dashboard
- **View Switching:** Toggle between day, week, and month calendar views
- **Dynamic Date Validation:** Parse and validate date headers with month/year from DOM attributes
- **Meeting Creation:** Create meetings/notes with custom summaries
- **Meeting Editing:** Edit existing meeting information with text updates
- **Tag Management:** Select and manage meeting tags

### Key Transformations from Java

1. **Wait Strategy Improvements:**
   - Replaced `WebDriverWait(Driver.getDriver(), 2)` with context-based waits from BasePage
   - Eliminated all `Thread.sleep(3000)` calls
   - Replaced with explicit `wait_for_visibility` using `expected_conditions`

2. **Month Name Conversion:**
   - Java: Verbose 40-line switch-case statement (lines 59-96, 115-152)
   - Python: Single-line `calendar.month_name[month_index]` lookup
   - More maintainable and Pythonic approach

3. **Assertion Pattern:**
   - Java: `Assert.assertEquals(expected, actual, message)`
   - Python: `assert actual == expected, message`
   - Native Python assertion with clear error messages

4. **Exception Handling:**
   - Java: `InterruptedException` declarations removed
   - Python: Native exception handling with proper timeout management

5. **Element Access:**
   - Property-based element access prevents stale element exceptions
   - Fresh WebElement references on each access through `@property` decorators

### Technical Improvements

- **Comprehensive Logging:** Module-level logger with debug, info, and error levels for test diagnostics
- **Explicit Waits Only:** All waits use `WebDriverWait` with `expected_conditions` (no implicit waits)
- **Thread Safety:** Compatible with parallel execution via context-based driver access
- **Data-Driven Validation:** Dynamic date parsing from DOM attributes instead of hard-coded values

---

## Step Definitions

### Navigation Steps

#### user_clicks_on_the_calendar_dashboard

Navigate to the calendar module by clicking the calendar dashboard button.

**Decorator:** `@when("User click on the calendar dashboard")`

**Function Signature:**
```python
def user_clicks_on_the_calendar_dashboard(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If calendar button not clickable or not visible after click

**Description:**

Waits for the calendar button to be clickable, performs click action, and verifies the calendar button remains visible after navigation (confirming the calendar module loaded successfully).

**Technical Notes:**
- Replaces Java line 19: `calendarP.calendarButton.click()`
- Replaces Java line 20: `wait.until(ExpectedConditions.visibilityOf())`
- Uses property-based element access to get fresh WebElement reference

**Usage Example:**

```gherkin
Scenario: Navigate to calendar
  When User click on the calendar dashboard
  Then User should see the last stage of calendar view
```

**Source:** `features/steps/calendar_steps.py:57-89`

**CalendarPage Interactions:**
- `calendar_page.calendar_button.click()` - Click calendar navigation button
- Waits for `calendar_page.calendar_button` visibility confirmation

---

#### user_clicks_on_day_button

Switch calendar view to day mode.

**Decorator:** `@when("User click on day button")`

**Function Signature:**
```python
def user_clicks_on_day_button(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If day button not clickable or not visible after click

**Description:**

Clicks the 'Day' button and waits for it to remain visible, confirming the view switch completed successfully.

**Technical Notes:**
- Replaces Java lines 25-26: day button click with visibility wait
- No `Thread.sleep()` - uses explicit wait instead

**Usage Example:**

```gherkin
Scenario: Switch to day view
  When User click on the calendar dashboard
  And User click on day button
  Then User should see the last stage of calendar view
```

**Source:** `features/steps/calendar_steps.py:92-121`

**CalendarPage Interactions:**
- `calendar_page.day.click()` - Click day view button
- Waits for `calendar_page.day` visibility confirmation

---

#### user_clicks_on_week_button

Switch calendar view to week mode.

**Decorator:** `@when("User click on week button")`

**Function Signature:**
```python
def user_clicks_on_week_button(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If week button not clickable or not visible after click

**Description:**

Clicks the 'Week' button and waits for it to remain visible, confirming the view switch completed successfully.

**Technical Notes:**
- Replaces Java lines 31-32: week button click with visibility wait
- No `Thread.sleep()` - uses explicit wait instead

**Usage Example:**

```gherkin
Scenario: Switch to week view
  When User click on the calendar dashboard
  And User click on week button
  Then User should see the last stage of calendar view
```

**Source:** `features/steps/calendar_steps.py:124-153`

**CalendarPage Interactions:**
- `calendar_page.week.click()` - Click week view button
- Waits for `calendar_page.week` visibility confirmation

---

#### user_clicks_on_month_button

Switch calendar view to month mode.

**Decorator:** `@when("User click on month button")`

**Function Signature:**
```python
def user_clicks_on_month_button(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If month button not clickable or not visible after click

**Description:**

Clicks the 'Month' button and waits for it to remain visible, confirming the view switch completed successfully.

**Technical Notes:**
- Replaces Java lines 37-38: month button click with visibility wait
- No `Thread.sleep()` - uses explicit wait instead

**Usage Example:**

```gherkin
Scenario: Switch to month view
  When User click on the calendar dashboard
  And User click on month button
  Then User should see the last stage of calendar view
```

**Source:** `features/steps/calendar_steps.py:156-185`

**CalendarPage Interactions:**
- `calendar_page.month.click()` - Click month view button
- Waits for `calendar_page.month` visibility confirmation

---

### Verification Steps

#### user_should_see_the_last_stage_of_calendar_view

Verify calendar module fully loaded by checking calendar container visibility and page title.

**Decorator:** `@then("User should see the last stage of calendar view")`

**Function Signature:**
```python
def user_should_see_the_last_stage_of_calendar_view(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If calendar module not visible within timeout
- `AssertionError`: If page title doesn't match expected value

**Description:**

Validates that:
1. Calendar container module is visible on the page
2. Page title matches "Meetings - Odoo"

**Technical Notes:**
- Replaces Java lines 43-46: calendar module visibility and title assertion
- Uses Python `assert` instead of JUnit `Assert.assertEquals`

**Usage Example:**

```gherkin
Scenario: Verify all buttons work
  When User click on the calendar dashboard
  And User click on day button
  And User click on week button
  And User click on month button
  Then User should see the last stage of calendar view
```

**Source:** `features/steps/calendar_steps.py:188-227`

**CalendarPage Interactions:**
- Waits for `calendar_page.calendar_module` visibility
- Validates page title via `context.driver.title`

---

### Date Validation Steps

#### user_clicks_day_on_the_calendar_and_display_day

Switch to day view and validate the displayed date header format.

**Decorator:** `@when("User click day on the calendar and display day")`

**Function Signature:**
```python
def user_clicks_day_on_the_calendar_and_display_day(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If day button or date elements not found
- `AssertionError`: If actual date header doesn't match expected format

**Description:**

Performs comprehensive date validation workflow:
1. Clicks day button to switch to day view
2. Waits for day button visibility confirmation
3. Extracts day number, month, and year from calendar DOM attributes
4. Converts month number to month name using `calendar.month_name`
5. Validates date header matches format: "Meetings (Month Day, Year)"

**Technical Notes:**
- Replaces Java lines 51-101: day view with dynamic date validation
- Eliminates `Thread.sleep(3000)` - uses explicit waits instead
- Replaces verbose Java switch-case (lines 59-96) with `calendar.month_name`
- `data-month` attribute is 0-indexed, so add 1 for `calendar.month_name`

**Date Format Example:**

DOM attributes: `data-month="10"`, `data-year="2024"`, day text="7"

Expected header: `"Meetings (November 7, 2024)"`

**Usage Example:**

```gherkin
Scenario: Validate day view date
  When User click on the calendar dashboard
  And User click day on the calendar and display day
```

**Source:** `features/steps/calendar_steps.py:230-300`

**CalendarPage Interactions:**
- `calendar_page.day.click()` - Switch to day view
- `calendar_page.day_calendar.text` - Extract day number
- `calendar_page.month_and_year_calendar.get_attribute("data-month")` - Extract month (0-indexed)
- `calendar_page.month_and_year_calendar.get_attribute("data-year")` - Extract year
- `calendar_page.date_actual.text` - Get displayed date header for validation

---

#### user_click_month_on_the_calendar_and_display_month

Switch to month view and validate the displayed date header format.

**Decorator:** `@then("User click month on the calendar and display month")`

**Function Signature:**
```python
def user_click_month_on_the_calendar_and_display_month(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If month button or date elements not found
- `AssertionError`: If actual date header doesn't match expected format

**Description:**

Performs comprehensive month view date validation:
1. Clicks month button to switch to month view
2. Waits for month button visibility confirmation
3. Extracts month and year from calendar DOM attributes
4. Converts month number to month name using `calendar.month_name`
5. Validates date header matches format: "Meetings (Month Year)"

**Technical Notes:**
- Replaces Java lines 107-157: month view with dynamic date validation
- Eliminates `Thread.sleep(3000)` - uses explicit waits instead
- Replaces verbose Java switch-case (lines 115-152) with `calendar.month_name`
- `data-month` attribute is 0-indexed, so add 1 for `calendar.month_name`

**Date Format Example:**

DOM attributes: `data-month="10"`, `data-year="2024"`

Expected header: `"Meetings (November 2024)"`

**Usage Example:**

```gherkin
Scenario: Validate month view date
  When User click on the calendar dashboard
  Then User click month on the calendar and display month
```

**Source:** `features/steps/calendar_steps.py:303-369`

**CalendarPage Interactions:**
- `calendar_page.month.click()` - Switch to month view
- `calendar_page.month_and_year_calendar.get_attribute("data-month")` - Extract month (0-indexed)
- `calendar_page.month_and_year_calendar.get_attribute("data-year")` - Extract year
- `calendar_page.date_actual.text` - Get displayed date header for validation

---

### Meeting Management Steps

#### user_click_on_desired_date_time

Click on a specific date cell to open the meeting creation dialog.

**Decorator:** `@step("User click on desired date time")`

**Function Signature:**
```python
def user_click_on_desired_date_time(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If date box not clickable or create note modal not visible
- `AssertionError`: If create note modal is not displayed

**Description:**

Clicks the date box (calendar cell) and verifies that the note creation modal header becomes visible, confirming the creation dialog opened successfully.

**Technical Notes:**
- Replaces Java lines 161-163: date box click with modal verification
- Uses `@step` decorator (works for @And, @Given, @When, @Then in Gherkin)
- **TECHNICAL DEBT:** `date_box` uses brittle index-based XPath [29]

**Usage Example:**

```gherkin
Scenario: Create a meeting
  When User click on the calendar dashboard
  And User click day on the calendar and display day
  And User click on desired date time
  Then User enters "Team Standup" in the box and clicks the create button
```

**Source:** `features/steps/calendar_steps.py:372-408`

**CalendarPage Interactions:**
- `calendar_page.date_box.click()` - Click date cell to open creation dialog
- Waits for `calendar_page.create_note` modal visibility
- Validates `calendar_page.create_note.is_displayed()`

---

#### user_enters_note_in_the_box_and_clicks_the_create_button

Enter meeting summary and create the meeting/note.

**Decorator:** `@then('User enters "{note}" in the box and clicks the create button')`

**Function Signature:**
```python
def user_enters_note_in_the_box_and_clicks_the_create_button(context, note):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state
- `note` (str): Meeting/note summary text to enter (captured from Gherkin step)

**Raises:**
- `TimeoutException`: If summary box or create button not found
- `AssertionError`: If created note text doesn't match input

**Description:**

Performs the complete meeting creation workflow:
1. Enters the provided note text into the summary box
2. Clicks the create button to save the meeting
3. Validates the created note text matches the input

**Technical Notes:**
- Replaces Java lines 167-174: note creation with validation
- Parameter captured from Gherkin step text `{string}` placeholder
- Validates note creation by comparing input with displayed note

**Usage Example:**

```gherkin
Scenario: Create event with custom summary
  When User click on desired date time
  Then User enters "Team Standup Meeting" in the box and clicks the create button
```

**Scenario Outline Example:**

```gherkin
Scenario Outline: Create multiple events
  When User click on desired date time
  Then User enters "<test>" in the box and clicks the create button
  
  Examples:
    | test          |
    | Test test     |
    | Sprint Review |
```

**Source:** `features/steps/calendar_steps.py:411-463`

**CalendarPage Interactions:**
- `calendar_page.summary_box.send_keys(note)` - Enter meeting summary
- `calendar_page.create_button.click()` - Save meeting
- Waits for `calendar_page.get_note` visibility
- Validates `calendar_page.get_note.text` matches input

---

#### user_can_see_all_the_note

Verify the created note is visible in the calendar view.

**Decorator:** `@when("User can see all the note")`

**Function Signature:**
```python
def user_can_see_all_the_note(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If created note element not found
- `AssertionError`: If created note is not displayed

**Description:**

Validates that the created note element is displayed, confirming the meeting/note was successfully created and is visible in the calendar view.

**Technical Notes:**
- Replaces Java lines 178-179: created note visibility validation
- Uses `is_displayed()` to verify element is visible on page

**Usage Example:**

```gherkin
Scenario: Verify created event is visible
  When User enters "Test" in the box and clicks the create button
  And User can see all the note
```

**Source:** `features/steps/calendar_steps.py:466-498`

**CalendarPage Interactions:**
- Waits for `calendar_page.created_note` visibility
- Validates `calendar_page.created_note.is_displayed()`

---

#### user_can_select_the_note

Select an existing note to open its details modal.

**Decorator:** `@when("User can select the note")`

**Function Signature:**
```python
def user_can_select_the_note(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If select note element not found
- `AssertionError`: If modal content is not displayed

**Description:**

Performs note selection workflow:
1. Clicks on the note to select it
2. Waits for select note element visibility confirmation
3. Verifies the modal content is displayed

**Technical Notes:**
- Replaces Java lines 182-185: note selection with modal verification
- Uses wait to ensure note selection completed before validation

**Usage Example:**

```gherkin
Scenario: Select and view event details
  When User can see all the note
  And User can select the note
  Then User can edit the information
```

**Source:** `features/steps/calendar_steps.py:501-541`

**CalendarPage Interactions:**
- `calendar_page.select_note.click()` - Click note to select
- Waits for `calendar_page.select_note` visibility confirmation
- Waits for `calendar_page.created_modele` modal visibility
- Validates `calendar_page.created_modele.is_displayed()`

---

#### user_can_edit_the_information

Edit the selected meeting/note information.

**Decorator:** `@when("User can edit the information")`

**Function Signature:**
```python
def user_can_edit_the_information(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If edit button or edit text field not found

**Description:**

Performs comprehensive meeting editing workflow:
1. Clicks the edit button to enable editing mode
2. Waits for edit button visibility confirmation
3. Clears existing text from edit field
4. Enters new text "Hello My Friends"
5. Waits for edit text visibility
6. Checks if tags checkbox is selected (validation step)

**Technical Notes:**
- Replaces Java lines 188-195: note editing workflow
- Uses explicit waits after each action to ensure completion
- Tags checkbox selection check (line 194) doesn't modify state

**Usage Example:**

```gherkin
Scenario: Edit existing event
  When User can select the note
  And User can edit the information
  Then User can save all edit
```

**Source:** `features/steps/calendar_steps.py:544-596`

**CalendarPage Interactions:**
- `calendar_page.edit_button.click()` - Enable editing mode
- Waits for `calendar_page.edit_button` visibility
- `calendar_page.edit_text.clear()` - Clear existing text
- `calendar_page.edit_text.send_keys("Hello My Friends")` - Enter new text
- Waits for `calendar_page.edit_text` visibility
- `calendar_page.tags_checkbox.is_selected()` - Check tag selection status

---

#### user_can_save_all_edit

Save the edited meeting/note information.

**Decorator:** `@then("User can save all edit")`

**Function Signature:**
```python
def user_can_save_all_edit(context):
```

**Parameters:**
- `context` (behave.runner.Context): Behave context object containing driver and shared state

**Raises:**
- `TimeoutException`: If save button not clickable

**Description:**

Clicks the save button to persist changes made to the meeting/note. Finalizes the editing workflow started in `user_can_edit_the_information`.

**Technical Notes:**
- Replaces Java lines 199-200: save button click
- Finalizes the editing workflow

**Usage Example:**

```gherkin
Scenario: Complete event editing
  When User can edit the information
  Then User can save all edit
```

**Source:** `features/steps/calendar_steps.py:599-628`

**CalendarPage Interactions:**
- `calendar_page.save_button.click()` - Persist changes

---

## Complete Usage Examples

### Scenario 1: Verify All Calendar View Buttons

```gherkin
@Calendar
Scenario: Verify that all buttons work as expected at the Calendar stage
  When User click on the calendar dashboard
  And User click on day button
  And User click on week button
  And User click on month button
  Then User should see the last stage of calendar view
```

**Step-to-Code Mapping:**
1. `When User click on the calendar dashboard` → `user_clicks_on_the_calendar_dashboard()`
2. `And User click on day button` → `user_clicks_on_day_button()`
3. `And User click on week button` → `user_clicks_on_week_button()`
4. `And User click on month button` → `user_clicks_on_month_button()`
5. `Then User should see the last stage of calendar view` → `user_should_see_the_last_stage_of_calendar_view()`

---

### Scenario 2: Change Display Between Day-Week-Month

```gherkin
@Calendar
Scenario: User can change display between Day-Week-Month
  When User click on the calendar dashboard
  And User click day on the calendar and display day
  Then User click month on the calendar and display month
```

**Step-to-Code Mapping:**
1. `When User click on the calendar dashboard` → `user_clicks_on_the_calendar_dashboard()`
2. `And User click day on the calendar and display day` → `user_clicks_day_on_the_calendar_and_display_day()`
3. `Then User click month on the calendar and display month` → `user_click_month_on_the_calendar_and_display_month()`

**Key Feature:** Dynamic date validation with month/year parsing from DOM attributes

---

### Scenario 3: Create Event Using Scenario Outline

```gherkin
@Calendar
Scenario Outline: User can create event by clicking on daily time box
  When User click on the calendar dashboard
  And User click day on the calendar and display day
  And User click on desired date time
  Then User enters "<test>" in the box and clicks the create button

  Examples: Test name
    |test       |
    |Test test  |
```

**Step-to-Code Mapping:**
1. `When User click on the calendar dashboard` → `user_clicks_on_the_calendar_dashboard()`
2. `And User click day on the calendar and display day` → `user_clicks_day_on_the_calendar_and_display_day()`
3. `And User click on desired date time` → `user_click_on_desired_date_time()`
4. `Then User enters "<test>" in the box and clicks the create button` → `user_enters_note_in_the_box_and_clicks_the_create_button(context, note="Test test")`

**Key Feature:** Data-driven testing with parameterized note text

---

### Scenario 4: Edit Created Event

```gherkin
@Calendar
Scenario: User can edit a created event
  When User click on the calendar dashboard
  And User click day on the calendar and display day
  And User click on desired date time
  And User enters "Test" in the box and clicks the create button
  And User can see all the note
  And User can select the note
  And User can edit the information
  Then User can save all edit
```

**Step-to-Code Mapping:**
1. `When User click on the calendar dashboard` → `user_clicks_on_the_calendar_dashboard()`
2. `And User click day on the calendar and display day` → `user_clicks_day_on_the_calendar_and_display_day()`
3. `And User click on desired date time` → `user_click_on_desired_date_time()`
4. `And User enters "Test" in the box and clicks the create button` → `user_enters_note_in_the_box_and_clicks_the_create_button(context, note="Test")`
5. `And User can see all the note` → `user_can_see_all_the_note()`
6. `And User can select the note` → `user_can_select_the_note()`
7. `And User can edit the information` → `user_can_edit_the_information()`
8. `Then User can save all edit` → `user_can_save_all_edit()`

**Key Feature:** Complete meeting lifecycle (create → view → select → edit → save)

---

## Integration with CalendarPage

All step definitions interact with the `CalendarPage` page object, which is instantiated in each step using:

```python
from pages.calendar_page import CalendarPage

calendar_page = CalendarPage(context.driver)
```

### Key CalendarPage Elements Used

| Element Property | Purpose | Used By Steps |
|-----------------|---------|---------------|
| `calendar_button` | Navigate to calendar module | `user_clicks_on_the_calendar_dashboard` |
| `day` | Switch to day view | `user_clicks_on_day_button`, `user_clicks_day_on_the_calendar_and_display_day` |
| `week` | Switch to week view | `user_clicks_on_week_button` |
| `month` | Switch to month view | `user_clicks_on_month_button`, `user_click_month_on_the_calendar_and_display_month` |
| `calendar_module` | Calendar container for visibility validation | `user_should_see_the_last_stage_of_calendar_view` |
| `day_calendar` | Current day number text | `user_clicks_day_on_the_calendar_and_display_day` |
| `month_and_year_calendar` | Element with data-month and data-year attributes | Both date validation steps |
| `date_actual` | Date header text for validation | Both date validation steps |
| `date_box` | Calendar cell to click for event creation | `user_click_on_desired_date_time` |
| `create_note` | Meeting creation modal header | `user_click_on_desired_date_time` |
| `summary_box` | Meeting summary input field | `user_enters_note_in_the_box_and_clicks_the_create_button` |
| `create_button` | Save new meeting button | `user_enters_note_in_the_box_and_clicks_the_create_button` |
| `get_note` | Created note element for validation | `user_enters_note_in_the_box_and_clicks_the_create_button` |
| `created_note` | Created note in calendar view | `user_can_see_all_the_note` |
| `select_note` | Note element to click for selection | `user_can_select_the_note` |
| `created_modele` | Note details modal content | `user_can_select_the_note` |
| `edit_button` | Enable editing mode button | `user_can_edit_the_information` |
| `edit_text` | Editable text field | `user_can_edit_the_information` |
| `tags_checkbox` | Tag selection checkbox | `user_can_edit_the_information` |
| `save_button` | Save edited meeting button | `user_can_save_all_edit` |

---

## Migration Notes

### Java to Python Pattern Transformations

**1. Month Name Conversion - Eliminated Verbose Switch-Case**

**Java (Lines 59-96, 115-152):**
```java
String month;
switch (monthValue) {
    case 0:
        month = "January";
        break;
    case 1:
        month = "February";
        break;
    // ... 10 more cases ...
    default:
        month = "Unknown";
}
```

**Python:**
```python
import calendar
month = calendar.month_name[month_calendar]  # Single line!
```

**Benefits:**
- 40+ lines reduced to 1 line
- No maintenance of month name strings
- Uses Python standard library
- More readable and Pythonic

---

**2. Wait Strategy - Eliminated Thread.sleep()**

**Java:**
```java
Thread.sleep(3000);  // Hard-coded 3-second delay
```

**Python:**
```python
wait = WebDriverWait(context.driver, 10)
wait.until(EC.visibility_of(calendar_page.element))
```

**Benefits:**
- No arbitrary delays
- Fails fast if element not found
- Waits only as long as necessary (up to timeout)
- More reliable for varying page load speeds

---

**3. Assertion Pattern**

**Java:**
```java
Assert.assertEquals("Meetings - Odoo", context.driver.getTitle(), 
                    "The title is not same as the expected!");
```

**Python:**
```python
expected_dashboard = "Meetings - Odoo"
actual_dashboard = context.driver.title
assert actual_dashboard == expected_dashboard, \
    f"The title is not same as the expected! Expected: '{expected_dashboard}', Got: '{actual_dashboard}'"
```

**Benefits:**
- Native Python assertion syntax
- Clear f-string formatting
- Explicit variable names improve readability

---

**4. Driver Access Pattern**

**Java:**
```java
CalendarPage calendarP = new CalendarPage();
calendarP.calendarButton.click();  // Uses static Driver.getDriver()
```

**Python:**
```python
calendar_page = CalendarPage(context.driver)
calendar_page.calendar_button.click()  # Explicit driver passing
```

**Benefits:**
- Explicit dependency injection
- Better for parallel execution
- Context-based driver management
- Thread-safe with `threading.local()`

---

## Thread Safety Considerations

All step definitions are **thread-safe** for parallel test execution:

1. **Context-Based Driver Access:** Each scenario gets its own `context` object with independent `context.driver`
2. **No Shared State:** CalendarPage instantiated fresh in each step
3. **No Module-Level Variables:** All state contained in function scope or context
4. **Logger Thread-Safe:** Python logging module is thread-safe by default

**Parallel Execution Example:**

```bash
# Run calendar tests in parallel using behave-parallel
behave --tags=@Calendar --processes 4
```

---

## Troubleshooting

### Common Issues

#### Issue: Date header validation fails with "Date header mismatch"

**Symptoms:**
```
AssertionError: Date header mismatch! Expected: 'Meetings (November 7, 2024)', Got: 'Meetings (November 8, 2024)'
```

**Cause:** Test execution crosses midnight boundary, or calendar defaults to different date

**Solution:**
- Ensure tests run during same date
- Consider parameterizing expected date instead of hard-coding
- Add date synchronization logic if needed

---

#### Issue: TimeoutException on calendar_page.date_box.click()

**Symptoms:**
```
TimeoutException: Message: Element not found: date_box
```

**Cause:** `date_box` uses brittle index-based XPath `[29]`

**Solution:**
- Verify calendar is in day view before clicking date box
- Ensure sufficient wait time for calendar to render
- Consider updating locator strategy to use dynamic date selection

---

#### Issue: created_note.text doesn't match input note

**Symptoms:**
```
AssertionError: Created note text doesn't match! Expected: 'Team Standup', Got: 'Team Standup Meeting'
```

**Cause:** Application may auto-append text or use different display format

**Solution:**
- Use `assertIn()` for partial text matching instead of exact match
- Verify application behavior in manual test
- Update assertion to match actual application behavior

---

## See Also

- **[CalendarPage API Reference](../pages/calendar-page.md)** - Page object for calendar interactions
- **[Calendar Testing Guide](../../guides/calendar-testing.md)** - Comprehensive calendar testing workflows
- **[Step Definitions Guide](../../guides/step-definitions.md)** - Writing custom step definitions
- **[Behave Configuration](../../reference/behave-configuration.md)** - Behave framework configuration
- **[Wait Strategies Guide](../../guides/wait-strategies.md)** - Best practices for explicit waits
- **[Feature Files Guide](../../guides/feature-files.md)** - Writing Gherkin scenarios

---

**Last Updated:** 2024 (Migrated from Java Calendar.java)

**Module Maintainers:** Testinium QA Team

**Related Feature File:** `features/Calendar.feature`
