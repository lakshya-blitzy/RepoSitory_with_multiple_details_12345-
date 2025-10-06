"""
Calendar Step Definitions Module

Behave step definitions for calendar and meeting management test scenarios.
Converted from Calendar.java with comprehensive wait strategies replacing Thread.sleep().

Key Features:
- Calendar module navigation and view switching (day/week/month)
- Dynamic date header validation with month/year attribute parsing
- Meeting/note creation with summary input
- Meeting/note editing workflows
- Tag selection and management

Migration Context:
    Java Source: src/main/java/com/testinium/step_definitions/Calendar.java
    Migration Type: Cucumber @When/@Then/@And → Behave @when/@then/@step
    Pattern: Static Driver.getDriver() → context.driver pattern
    
Key Transformations:
    1. Replaced WebDriverWait(Driver.getDriver(), 2) with context-based waits from BasePage
    2. Eliminated Thread.sleep(3000) calls, replaced with explicit wait_for_visibility
    3. Converted Java switch-case month mapping to Python calendar.month_name lookup
    4. Replaced Assert.assertEquals with Python assert statements
    5. Converted calendarP instance to calendar_page = CalendarPage(context.driver)
    6. Removed InterruptedException declarations (not needed in Python)

Technical Improvements:
    - All waits now use explicit WebDriverWait with expected conditions
    - Cleaner month name conversion using Python standard library
    - Comprehensive logging for test diagnostics
    - Property-based element access prevents stale element exceptions

Example Gherkin:
    Scenario: View calendar in different modes
        When User click on the calendar dashboard
        And User click on day button
        Then User should see the last stage of calendar view

    Scenario: Create a meeting
        When User click on desired date time
        Then User enters "Team Standup" in the box and clicks the create button
        When User can see all the note
"""

import calendar
import logging
from behave import when, then, step
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.calendar_page import CalendarPage

# Configure module-level logger
logger = logging.getLogger(__name__)


@when("User click on the calendar dashboard")
def user_clicks_on_the_calendar_dashboard(context):
    """
    Navigate to the calendar module by clicking the calendar dashboard button.
    
    Waits for calendar button to be clickable, performs click action, and verifies
    the calendar button remains visible after navigation (confirming module loaded).
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If calendar button not clickable or not visible after click
        
    Technical Notes:
        - Replaces Java line 19: calendarP.calendarButton.click()
        - Replaces Java line 20: wait.until(ExpectedConditions.visibilityOf())
        - Uses property-based element access to get fresh WebElement reference
    """
    logger.info("Step: User clicks on the calendar dashboard")
    
    # Initialize page object with context driver
    calendar_page = CalendarPage(context.driver)
    
    # Click calendar button and wait for visibility confirmation
    logger.debug("Clicking calendar button to navigate to calendar module")
    calendar_page.calendar_button.click()
    
    # Verify calendar button remains visible (confirms successful navigation)
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.calendar_button))
    
    logger.info("Successfully navigated to calendar dashboard")


@when("User click on day button")
def user_clicks_on_day_button(context):
    """
    Switch calendar view to day mode.
    
    Clicks the 'Day' button and waits for it to remain visible, confirming
    the view switch completed successfully.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If day button not clickable or not visible after click
        
    Technical Notes:
        - Replaces Java lines 25-26: day button click with visibility wait
        - No Thread.sleep() - uses explicit wait instead
    """
    logger.info("Step: User clicks on day button")
    
    calendar_page = CalendarPage(context.driver)
    
    logger.debug("Clicking day button to switch to day view")
    calendar_page.day.click()
    
    # Wait for day button to remain visible (confirms view changed)
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.day))
    
    logger.info("Successfully switched to day view")


@when("User click on week button")
def user_clicks_on_week_button(context):
    """
    Switch calendar view to week mode.
    
    Clicks the 'Week' button and waits for it to remain visible, confirming
    the view switch completed successfully.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If week button not clickable or not visible after click
        
    Technical Notes:
        - Replaces Java lines 31-32: week button click with visibility wait
        - No Thread.sleep() - uses explicit wait instead
    """
    logger.info("Step: User clicks on week button")
    
    calendar_page = CalendarPage(context.driver)
    
    logger.debug("Clicking week button to switch to week view")
    calendar_page.week.click()
    
    # Wait for week button to remain visible (confirms view changed)
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.week))
    
    logger.info("Successfully switched to week view")


@when("User click on month button")
def user_clicks_on_month_button(context):
    """
    Switch calendar view to month mode.
    
    Clicks the 'Month' button and waits for it to remain visible, confirming
    the view switch completed successfully.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If month button not clickable or not visible after click
        
    Technical Notes:
        - Replaces Java lines 37-38: month button click with visibility wait
        - No Thread.sleep() - uses explicit wait instead
    """
    logger.info("Step: User clicks on month button")
    
    calendar_page = CalendarPage(context.driver)
    
    logger.debug("Clicking month button to switch to month view")
    calendar_page.month.click()
    
    # Wait for month button to remain visible (confirms view changed)
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.month))
    
    logger.info("Successfully switched to month view")


@then("User should see the last stage of calendar view")
def user_should_see_the_last_stage_of_calendar_view(context):
    """
    Verify calendar module fully loaded by checking calendar container visibility
    and page title.
    
    Validates that:
    1. Calendar container module is visible on the page
    2. Page title matches "Meetings - Odoo"
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If calendar module not visible within timeout
        AssertionError: If page title doesn't match expected value
        
    Technical Notes:
        - Replaces Java lines 43-46: calendar module visibility and title assertion
        - Uses Python assert instead of JUnit Assert.assertEquals
    """
    logger.info("Step: Verifying last stage of calendar view")
    
    calendar_page = CalendarPage(context.driver)
    
    # Wait for calendar module container to be visible
    wait = WebDriverWait(context.driver, 10)
    logger.debug("Waiting for calendar module container to be visible")
    wait.until(EC.visibility_of(calendar_page.calendar_module))
    
    # Verify page title matches expected value
    expected_dashboard = "Meetings - Odoo"
    actual_dashboard = context.driver.title
    
    logger.debug(f"Expected title: '{expected_dashboard}', Actual title: '{actual_dashboard}'")
    
    assert actual_dashboard == expected_dashboard, \
        f"The title is not same as the expected! Expected: '{expected_dashboard}', Got: '{actual_dashboard}'"
    
    logger.info("Successfully verified calendar view with correct title")


@when("User click day on the calendar and display day")
def user_clicks_day_on_the_calendar_and_display_day(context):
    """
    Switch to day view and validate the displayed date header format.
    
    Performs the following workflow:
    1. Clicks day button to switch to day view
    2. Waits for day button visibility confirmation
    3. Extracts day number, month, and year from calendar DOM attributes
    4. Converts month number to month name using calendar.month_name
    5. Validates date header matches format: "Meetings (Month Day, Year)"
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If day button or date elements not found
        AssertionError: If actual date header doesn't match expected format
        
    Technical Notes:
        - Replaces Java lines 51-101: day view with dynamic date validation
        - Eliminates Thread.sleep(3000) - uses explicit waits instead
        - Replaces verbose Java switch-case (lines 59-96) with calendar.month_name
        - data-month attribute is 0-indexed, so add 1 for calendar.month_name
        
    Example:
        DOM attributes: data-month="10", data-year="2024", day text="7"
        Expected header: "Meetings (November 7, 2024)"
    """
    logger.info("Step: User clicks day on calendar and displays day")
    
    calendar_page = CalendarPage(context.driver)
    
    # Click day button to switch to day view
    logger.debug("Clicking day button to switch to day view")
    calendar_page.day.click()
    
    # Wait for day button visibility (confirms view switched)
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.day))
    
    # Extract day number from highlighted day element
    day_calendar = calendar_page.day_calendar.text
    logger.debug(f"Extracted day from calendar: {day_calendar}")
    
    # Extract month and year from data attributes (0-indexed month, so add 1)
    month_calendar = int(calendar_page.month_and_year_calendar.get_attribute("data-month")) + 1
    year_calendar = int(calendar_page.month_and_year_calendar.get_attribute("data-year"))
    
    logger.debug(f"Extracted month index: {month_calendar}, year: {year_calendar}")
    
    # Convert month number to month name using Python calendar module
    # This replaces the verbose Java switch-case from lines 59-96
    month = calendar.month_name[month_calendar]
    logger.debug(f"Converted month number {month_calendar} to month name: '{month}'")
    
    # Build expected date header string
    expected_result = f"Meetings ({month} {day_calendar}, {year_calendar})"
    
    # Wait for date element to be visible and extract text
    wait.until(EC.visibility_of(calendar_page.date_actual))
    actual_result = calendar_page.date_actual.text
    
    logger.info(f"Expected date header: '{expected_result}'")
    logger.info(f"Actual date header: '{actual_result}'")
    
    # Validate date header matches expected format
    assert expected_result == actual_result, \
        f"Date header mismatch! Expected: '{expected_result}', Got: '{actual_result}'"
    
    logger.info("Successfully validated day view date header")


@then("User click month on the calendar and display month")
def user_click_month_on_the_calendar_and_display_month(context):
    """
    Switch to month view and validate the displayed date header format.
    
    Performs the following workflow:
    1. Clicks month button to switch to month view
    2. Waits for month button visibility confirmation
    3. Extracts month and year from calendar DOM attributes
    4. Converts month number to month name using calendar.month_name
    5. Validates date header matches format: "Meetings (Month Year)"
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If month button or date elements not found
        AssertionError: If actual date header doesn't match expected format
        
    Technical Notes:
        - Replaces Java lines 107-157: month view with dynamic date validation
        - Eliminates Thread.sleep(3000) - uses explicit waits instead
        - Replaces verbose Java switch-case (lines 115-152) with calendar.month_name
        - data-month attribute is 0-indexed, so add 1 for calendar.month_name
        
    Example:
        DOM attributes: data-month="10", data-year="2024"
        Expected header: "Meetings (November 2024)"
    """
    logger.info("Step: User clicks month on calendar and displays month")
    
    calendar_page = CalendarPage(context.driver)
    
    # Click month button to switch to month view
    logger.debug("Clicking month button to switch to month view")
    calendar_page.month.click()
    
    # Wait for month button visibility (confirms view switched)
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.month))
    
    # Extract month and year from data attributes (0-indexed month, so add 1)
    month_calendar = int(calendar_page.month_and_year_calendar.get_attribute("data-month")) + 1
    year_calendar = int(calendar_page.month_and_year_calendar.get_attribute("data-year"))
    
    logger.debug(f"Extracted month index: {month_calendar}, year: {year_calendar}")
    
    # Convert month number to month name using Python calendar module
    # This replaces the verbose Java switch-case from lines 115-152
    month = calendar.month_name[month_calendar]
    logger.debug(f"Converted month number {month_calendar} to month name: '{month}'")
    
    # Build expected date header string (month view format, no day)
    expected_result = f"Meetings ({month} {year_calendar})"
    
    # Wait for date element to be visible and extract text
    wait.until(EC.visibility_of(calendar_page.date_actual))
    actual_result = calendar_page.date_actual.text
    
    logger.info(f"Expected date header: '{expected_result}'")
    logger.info(f"Actual date header: '{actual_result}'")
    
    # Validate date header matches expected format
    assert expected_result == actual_result, \
        f"Date header mismatch! Expected: '{expected_result}', Got: '{actual_result}'"
    
    logger.info("Successfully validated month view date header")


@step("User click on desired date time")
def user_click_on_desired_date_time(context):
    """
    Click on a specific date cell to open the meeting creation dialog.
    
    Clicks the date box (calendar cell) and verifies that the note creation
    modal header becomes visible, confirming the creation dialog opened.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If date box not clickable or create note modal not visible
        AssertionError: If create note modal is not displayed
        
    Technical Notes:
        - Replaces Java lines 161-163: date box click with modal verification
        - Uses @step decorator (works for @And, @Given, @When, @Then)
        - TECHNICAL DEBT: date_box uses brittle index-based XPath [29]
    """
    logger.info("Step: User clicks on desired date time")
    
    calendar_page = CalendarPage(context.driver)
    
    # Click on date box to open meeting creation dialog
    logger.debug("Clicking on date box to open meeting creation dialog")
    calendar_page.date_box.click()
    
    # Wait for create note modal to be visible
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.create_note))
    
    # Verify modal is displayed
    assert calendar_page.create_note.is_displayed(), \
        "Create note modal is not displayed after clicking date box"
    
    logger.info("Successfully opened meeting creation dialog")


@then('User enters "{note}" in the box and clicks the create button')
def user_enters_note_in_the_box_and_clicks_the_create_button(context, note):
    """
    Enter meeting summary and create the meeting/note.
    
    Performs the following workflow:
    1. Enters the provided note text into the summary box
    2. Clicks the create button to save the meeting
    3. Validates the created note text matches the input
    
    Args:
        context: Behave context object containing driver and shared state
        note: Meeting/note summary text to enter
        
    Raises:
        TimeoutException: If summary box or create button not found
        AssertionError: If created note text doesn't match input
        
    Technical Notes:
        - Replaces Java lines 167-174: note creation with validation
        - Parameter captured from Gherkin step text {string} placeholder
        - Validates note creation by comparing input with displayed note
        
    Example Gherkin:
        Then User enters "Team Standup Meeting" in the box and clicks the create button
    """
    logger.info(f"Step: User enters '{note}' in the box and clicks create button")
    
    calendar_page = CalendarPage(context.driver)
    
    # Store event name for validation
    event_name = note
    
    # Enter note text into summary box
    logger.debug(f"Entering note text: '{note}'")
    calendar_page.summary_box.send_keys(note)
    
    # Click create button to save the meeting
    logger.debug("Clicking create button to save meeting")
    calendar_page.create_button.click()
    
    # Wait for note to be created and visible
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.get_note))
    
    # Validate created note text matches input
    created_note_text = calendar_page.get_note.text
    logger.debug(f"Created note text: '{created_note_text}'")
    
    assert created_note_text == event_name, \
        f"Created note text doesn't match! Expected: '{event_name}', Got: '{created_note_text}'"
    
    logger.info(f"Successfully created meeting: '{note}'")


@when("User can see all the note")
def user_can_see_all_the_note(context):
    """
    Verify the created note is visible in the calendar view.
    
    Validates that the created note element is displayed, confirming
    the meeting/note was successfully created and is visible.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If created note element not found
        AssertionError: If created note is not displayed
        
    Technical Notes:
        - Replaces Java lines 178-179: created note visibility validation
        - Uses is_displayed() to verify element is visible on page
    """
    logger.info("Step: User verifies all notes are visible")
    
    calendar_page = CalendarPage(context.driver)
    
    # Wait for created note to be visible
    wait = WebDriverWait(context.driver, 10)
    logger.debug("Waiting for created note to be visible")
    wait.until(EC.visibility_of(calendar_page.created_note))
    
    # Verify note is displayed
    assert calendar_page.created_note.is_displayed(), \
        "Created note is not displayed in calendar view"
    
    logger.info("Successfully verified created note is visible")


@when("User can select the note")
def user_can_select_the_note(context):
    """
    Select an existing note to open its details modal.
    
    Performs the following workflow:
    1. Clicks on the note to select it
    2. Waits for select note element visibility confirmation
    3. Verifies the modal content is displayed
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If select note element not found
        AssertionError: If modal content is not displayed
        
    Technical Notes:
        - Replaces Java lines 182-185: note selection with modal verification
        - Uses wait to ensure note selection completed before validation
    """
    logger.info("Step: User selects the note")
    
    calendar_page = CalendarPage(context.driver)
    
    # Click on note to select it
    logger.debug("Clicking on note to select it")
    calendar_page.select_note.click()
    
    # Wait for note selection to complete
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.select_note))
    
    # Verify modal content is displayed
    logger.debug("Verifying modal content is displayed")
    wait.until(EC.visibility_of(calendar_page.created_modele))
    
    assert calendar_page.created_modele.is_displayed(), \
        "Note modal content is not displayed after selection"
    
    logger.info("Successfully selected note and opened modal")


@when("User can edit the information")
def user_can_edit_the_information(context):
    """
    Edit the selected meeting/note information.
    
    Performs the following workflow:
    1. Clicks the edit button to enable editing mode
    2. Waits for edit button visibility confirmation
    3. Clears existing text from edit field
    4. Enters new text "Hello My Friends"
    5. Waits for edit text visibility
    6. Checks if tags checkbox is selected (validation step)
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If edit button or edit text field not found
        
    Technical Notes:
        - Replaces Java lines 188-195: note editing workflow
        - Uses explicit waits after each action to ensure completion
        - Tags checkbox selection check (line 194) doesn't modify state
    """
    logger.info("Step: User edits the information")
    
    calendar_page = CalendarPage(context.driver)
    
    # Click edit button to enable editing mode
    logger.debug("Clicking edit button to enable editing mode")
    calendar_page.edit_button.click()
    
    # Wait for edit button visibility confirmation
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.edit_button))
    
    # Clear existing text from edit field
    logger.debug("Clearing existing text from edit field")
    calendar_page.edit_text.clear()
    
    # Enter new text
    new_text = "Hello My Friends"
    logger.debug(f"Entering new text: '{new_text}'")
    calendar_page.edit_text.send_keys(new_text)
    
    # Wait for edit text field visibility
    wait.until(EC.visibility_of(calendar_page.edit_text))
    
    # Check if tags checkbox is selected (validation step from Java line 194)
    tags_selected = calendar_page.tags_checkbox.is_selected()
    logger.debug(f"Tags checkbox selected status: {tags_selected}")
    
    logger.info("Successfully edited meeting information")


@then("User can save all edit")
def user_can_save_all_edit(context):
    """
    Save the edited meeting/note information.
    
    Clicks the save button to persist changes made to the meeting/note.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If save button not clickable
        
    Technical Notes:
        - Replaces Java lines 199-200: save button click
        - Finalizes the editing workflow started in user_can_edit_the_information
    """
    logger.info("Step: User saves all edits")
    
    calendar_page = CalendarPage(context.driver)
    
    # Click save button to persist changes
    logger.debug("Clicking save button to persist changes")
    calendar_page.save_button.click()
    
    # Wait a moment for save operation to complete
    wait = WebDriverWait(context.driver, 10)
    # Note: In production, consider waiting for a success message or modal dismissal
    
    logger.info("Successfully saved all edits")


# Module self-documentation
if __name__ == "__main__":
    print("Calendar Step Definitions Module")
    print("\nConverted from: Calendar.java")
    print("Pattern: Cucumber @When/@Then/@And → Behave @when/@then/@step")
    print("\nStep Definitions Implemented:")
    print("  1. user_clicks_on_the_calendar_dashboard")
    print("  2. user_clicks_on_day_button")
    print("  3. user_clicks_on_week_button")
    print("  4. user_clicks_on_month_button")
    print("  5. user_should_see_the_last_stage_of_calendar_view")
    print("  6. user_clicks_day_on_the_calendar_and_display_day (with dynamic date validation)")
    print("  7. user_click_month_on_the_calendar_and_display_month (with dynamic date validation)")
    print("  8. user_click_on_desired_date_time")
    print("  9. user_enters_note_in_the_box_and_clicks_the_create_button")
    print("  10. user_can_see_all_the_note")
    print("  11. user_can_select_the_note")
    print("  12. user_can_edit_the_information")
    print("  13. user_can_save_all_edit")
    print("\nKey Improvements:")
    print("  ✓ Eliminated Thread.sleep() calls")
    print("  ✓ Replaced with explicit WebDriverWait")
    print("  ✓ Cleaner month name conversion using calendar.month_name")
    print("  ✓ Comprehensive logging for test diagnostics")
    print("  ✓ Property-based element access prevents stale elements")
