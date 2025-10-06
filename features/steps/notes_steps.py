"""
Notes Step Definitions Module

Behave step definitions for notes management test scenarios.
This module implements all Gherkin steps from Notes.feature including:
- Notes module navigation and access
- Note creation with tag entry and description input
- Note editing workflows with form interaction
- Save button validation with success message verification
- Drag-and-drop operations between note sections
- Notes list display confirmation

Migration Context:
    Converted from: src/main/java/com/testinium/step_definitions/Notes.java
    Original Pattern: Cucumber Java with @When/@Then annotations
    Target Pattern: Python Behave with @when/@then decorators
    
Key Transformations:
    1. Thread.sleep(2000) removed - replaced with explicit waits via page objects
    2. WebDriverWait(Driver.getDriver(), 20) replaced with context-based driver
    3. Actions class → ActionChains for drag-and-drop operations
    4. notesP/inventoryP instances → notes_page/inventory_page with context pattern
    5. Assert.assertEquals/assertTrue → Python assert statements with messages
    6. Keys.ENTER keyboard interaction preserved for tag entry
    7. Fixed typo: 'expecgedMessage' → 'expected_message'
    
Behavioral Preservation:
    - All step text preserved exactly matching Notes.feature Gherkin scenarios
    - All element interactions produce identical results to Java implementation
    - Drag-and-drop functionality maintains same behavior using ActionChains
    - Success message validation uses exact string 'Note created' matching
    
Thread Safety:
    This module is thread-safe when used with Behave's context object,
    which provides thread-local driver instances from DriverManager.
    Each step function receives its own context instance.

Example Usage:
    Feature: Notes Management
        Scenario: Create a new note with tags
            When User clicks the Notes module
            And User clicks create button in Notes module
            And User enters a tag name
            And User enters description
            And User clicks save button
            Then User sees the created new notes

Dependencies:
    - pages.notes_page.NotesPage: Main page object for notes interface
    - pages.inventory_page.InventoryPage: Provides save_btn for editing workflow
    - selenium.webdriver.common.keys.Keys: Keyboard interaction (ENTER key)
    - selenium.webdriver.common.action_chains.ActionChains: Drag-and-drop operations

Author: Blitzy Platform Migration Agent
Migration Date: 2024
Original Source: com.testinium.step_definitions.Notes
"""

import logging
from behave import when, then
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pages.notes_page import NotesPage
from pages.inventory_page import InventoryPage


# Configure module-level logger for step execution tracking
logger = logging.getLogger(__name__)


@when("User clicks the Notes module")
def user_clicks_the_notes_module(context):
    """
    Navigate to the Notes module by clicking the Notes navigation link.
    
    Original Java implementation included Thread.sleep(2000) which has been
    REMOVED per migration requirements to eliminate sleep anti-pattern.
    The page object's explicit waits provide proper element synchronization.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If Notes module link not found within timeout
        
    Example:
        When User clicks the Notes module
        
    Migration Notes:
        - Removed Thread.sleep(2000) from line 23 of Notes.java
        - Using notes_page.notes_module property with explicit wait
        - Property returns fresh WebElement reference preventing stale elements
    """
    logger.info("Step: User clicks the Notes module")
    
    # Initialize NotesPage with thread-local driver from context
    notes_page = NotesPage(context.driver)
    
    # Click notes module navigation link
    # Page object handles explicit wait for element presence
    logger.debug("Clicking notes module navigation link")
    notes_page.notes_module.click()
    
    logger.info("Successfully navigated to Notes module")


@when("User clicks create button in Notes module")
def user_clicks_create_button_in_notes_module(context):
    """
    Click the create button to initiate new note creation workflow.
    
    Original Java used WebDriverWait with 20-second timeout for visibility.
    Python version uses page object's wait_for_clickable ensuring button
    is both visible and enabled before interaction.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If create button not clickable within timeout
        
    Example:
        When User clicks create button in Notes module
        
    Migration Notes:
        - Converted WebDriverWait(Driver.getDriver(), 20) to page object wait
        - using wait_for_clickable for better reliability (visible + enabled)
        - Original wait.until(ExpectedConditions.visibilityOf()) on line 29
    """
    logger.info("Step: User clicks create button in Notes module")
    
    notes_page = NotesPage(context.driver)
    
    # creating_notes property uses wait_for_clickable ensuring button is ready
    logger.debug("Waiting for create button to be clickable")
    notes_page.creating_notes.click()
    
    logger.info("Successfully clicked create button")


@when("User enters a tag name")
def user_enters_a_tag_name(context):
    """
    Enter a tag name for note categorization with keyboard ENTER submission.
    
    Implements tag entry with Keys.ENTER keyboard interaction to submit
    the tag, then clicks tab index to move focus. This preserves the exact
    behavior from Java implementation including keyboard interaction pattern.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If tags input field not found within timeout
        
    Example:
        When User enters a tag name
        
    Migration Notes:
        - Preserved Keys.ENTER keyboard interaction from line 35
        - sendKeys("New Tag", Keys.ENTER) → send_keys with Keys.ENTER
        - Java: notesP.tagsN.sendKeys("New Tag", Keys.ENTER)
        - Python: notes_page.tags_n.send_keys("New Tag", Keys.ENTER)
        - Maintains tab_index click for focus management
    """
    logger.info("Step: User enters a tag name")
    
    notes_page = NotesPage(context.driver)
    
    # Enter tag with ENTER key to submit
    logger.debug("Entering tag 'New Tag' with ENTER key submission")
    notes_page.tags_n.send_keys("New Tag", Keys.ENTER)
    
    # Click tab index element for focus management
    logger.debug("Clicking tab index for focus management")
    notes_page.tab_index.click()
    
    logger.info("Successfully entered tag name")


@when("User enters description")
def user_enters_description(context):
    """
    Enter note description text and save the note.
    
    Enters description in the rich text editor and clicks save button
    to persist the note data. This step combines description entry with
    save action as implemented in original Java code.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If description editor or save button not found
        
    Example:
        When User enters description
        
    Migration Notes:
        - Original line 41: notesP.description.sendKeys("...")
        - Original line 42: notesP.saveBtn.click()
        - Combined description entry with save action per Java implementation
        - Description text preserved exactly from original
    """
    logger.info("Step: User enters description")
    
    notes_page = NotesPage(context.driver)
    
    # Enter description in rich text editor
    description_text = "This note is an example for the Testinium App"
    logger.debug(f"Entering description: {description_text}")
    notes_page.description.send_keys(description_text)
    
    # Click save button to persist note
    logger.debug("Clicking save button after description entry")
    notes_page.save_btn.click()
    
    logger.info("Successfully entered description and clicked save")


@when("User clicks save button")
def user_clicks_save_button(context):
    """
    Click the save button to persist note changes.
    
    Waits for save button to be visible and clickable before clicking.
    This is a separate save step for scenarios that need explicit save
    action without combined description entry.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If save button not clickable within timeout
        
    Example:
        When User clicks save button
        
    Migration Notes:
        - Original lines 46-47: wait + click pattern
        - WebDriverWait for visibility converted to wait_for_clickable
        - Provides better reliability ensuring button is enabled
    """
    logger.info("Step: User clicks save button")
    
    notes_page = NotesPage(context.driver)
    
    # save_btn property uses wait_for_clickable for visibility + enabled check
    logger.debug("Waiting for save button visibility and clicking")
    notes_page.save_btn.click()
    
    logger.info("Successfully clicked save button")


@then("User sees the created new notes")
def user_sees_the_created_new_notes(context):
    """
    Verify that note creation success message is displayed.
    
    Validates that the 'Note created' confirmation message appears after
    note save operation. Uses exact string matching as in original Java
    implementation with Assert.assertEquals.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If created message not visible within timeout
        AssertionError: If message text doesn't match expected value
        
    Example:
        Then User sees the created new notes
        
    Migration Notes:
        - Fixed typo from original: 'expecgedMessage' → 'expected_message'
        - Assert.assertEquals(actualMessage, expecgedMessage) on line 53
        - Converted to Python: assert actual_message == expected_message
        - Added descriptive error message for assertion failure
        - created_message property uses wait_for_visibility
    """
    logger.info("Step: User sees the created new notes")
    
    notes_page = NotesPage(context.driver)
    
    # Get actual message text from confirmation element
    logger.debug("Retrieving created message text")
    actual_message = notes_page.created_message.text
    
    # Expected message matches original Java exactly
    expected_message = "Note created"
    
    logger.debug(f"Actual message: '{actual_message}', Expected: '{expected_message}'")
    
    # Assert message matches with descriptive error
    assert actual_message == expected_message, (
        f"Note creation confirmation message mismatch. "
        f"Expected: '{expected_message}', Actual: '{actual_message}'"
    )
    
    logger.info("Successfully verified note created message")


@when("User clicks the edit button")
def user_clicks_the_edit_button(context):
    """
    Click the edit button to enter note editing mode.
    
    Clicks the app_k element which serves as the edit button for the
    specific note identified by 'BDD Approach Framework with Cucumber' text.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If edit button not found within timeout
        
    Example:
        When User clicks the edit button
        
    Migration Notes:
        - Original line 58: notesP.appK.click()
        - app_k is application identifier element with specific note title
        - XPath: //span[.='BDD Approach Framework with Cucumber']
    """
    logger.info("Step: User clicks the edit button")
    
    notes_page = NotesPage(context.driver)
    
    # Click application identifier element to edit specific note
    logger.debug("Clicking app_k element to enter edit mode")
    notes_page.app_k.click()
    
    logger.info("Successfully clicked edit button")


@when("User enters new description")
def user_enters_new_description(context):
    """
    Clear existing description and enter new description text.
    
    This step implements the note editing workflow:
    1. Clear existing description content
    2. Enter new description text
    3. Click save button (from InventoryPage per original implementation)
    4. Return to notes module
    
    NOTE: Original Java code uses inventoryP.saveBtn instead of notesP.saveBtn
    on line 65, indicating shared UI component. This is preserved for
    behavioral equivalence.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If description editor or save button not found
        
    Example:
        When User enters new description
        
    Migration Notes:
        - Original lines 63-66: clear, sendKeys, inventoryP.saveBtn, notesModule
        - Uses InventoryPage.save_btn (not NotesPage.save_btn) per original
        - This indicates shared save button component across modules
        - Description text preserved exactly: "FKASDFGASDFADSFADS"
    """
    logger.info("Step: User enters new description")
    
    notes_page = NotesPage(context.driver)
    inventory_page = InventoryPage(context.driver)
    
    # Clear existing description content
    logger.debug("Clearing existing description")
    notes_page.description.clear()
    
    # Enter new description text (preserving original test data)
    new_description = "FKASDFGASDFADSFADS"
    logger.debug(f"Entering new description: {new_description}")
    notes_page.description.send_keys(new_description)
    
    # Click save button from InventoryPage per original implementation
    # This indicates shared save button component across modules
    logger.debug("Clicking save button from InventoryPage")
    inventory_page.save_btn.click()
    
    # Return to notes module navigation
    logger.debug("Returning to notes module")
    notes_page.notes_module.click()
    
    logger.info("Successfully updated description and returned to notes module")


@then("User should see the Notes list")
def user_should_see_the_notes_list(context):
    """
    Verify that the Notes list is visible and displayed.
    
    Waits for notes module to be visible, clicks it, and verifies
    that it is displayed. Uses Assert.assertTrue pattern from original
    Java implementation.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If notes module not visible within timeout
        AssertionError: If notes module is not displayed
        
    Example:
        Then User should see the Notes list
        
    Migration Notes:
        - Original lines 71-73: wait for visibility, click, assertTrue
        - WebDriverWait converted to page object explicit wait
        - Assert.assertTrue(notesModule.isDisplayed()) on line 73
        - Converted to: assert notes_page.notes_module.is_displayed()
    """
    logger.info("Step: User should see the Notes list")
    
    notes_page = NotesPage(context.driver)
    
    # notes_module property includes explicit wait for element presence
    logger.debug("Waiting for notes module visibility and clicking")
    notes_module_element = notes_page.notes_module
    notes_module_element.click()
    
    # Verify notes module is displayed
    logger.debug("Verifying notes module is displayed")
    assert notes_module_element.is_displayed(), (
        "Notes module should be displayed but is not visible"
    )
    
    logger.info("Successfully verified Notes list is displayed")


@when("User move element from New section to Today section")
def user_move_element_from_new_section_to_today_section(context):
    """
    Perform drag-and-drop operation to move note from New table to Today table.
    
    Uses ActionChains to implement complex drag-and-drop operation:
    1. Click and hold source element (new_table)
    2. Pause briefly for drag initiation
    3. Move to target element (today_table)
    4. Pause for positioning
    5. Release mouse to complete drop
    6. Perform to execute action chain
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If source or target table elements not found
        
    Example:
        When User move element from New section to Today section
        
    Migration Notes:
        - Original line 79: Actions class with pause(2000) in milliseconds
        - Java: actions.clickAndHold().pause(2000).moveToElement().pause(2000).release().perform()
        - Python: ActionChains with pause() in seconds or explicit waits
        - Converted pause(2000ms) → pause(2) for 2 seconds
        - ActionChains.pause() available in Selenium 4.x
    """
    logger.info("Step: User move element from New section to Today section")
    
    notes_page = NotesPage(context.driver)
    
    # Get source and target elements with explicit waits via page object
    logger.debug("Retrieving source element (new_table)")
    source_element = notes_page.new_table
    
    logger.debug("Retrieving target element (today_table)")
    target_element = notes_page.today_table
    
    # Initialize ActionChains with driver from context
    logger.debug("Initializing ActionChains for drag-and-drop operation")
    actions = ActionChains(context.driver)
    
    # Perform drag-and-drop with pauses for visual feedback
    logger.debug("Executing drag-and-drop: new_table → today_table")
    actions.click_and_hold(source_element).pause(2).move_to_element(target_element).pause(2).release().perform()
    
    logger.info("Successfully completed drag-and-drop operation")


@then("User sees Today new added element")
def user_sees_today_new_added_element(context):
    """
    Verify that the Today table contains the expected element.
    
    Validates that the today_table element displays the text 'Today'
    after the drag-and-drop operation. Uses exact string matching
    as in original Assert.assertEquals.
    
    Args:
        context: Behave context object containing driver and shared state
        
    Raises:
        TimeoutException: If today_table element not found within timeout
        AssertionError: If table text doesn't match expected value
        
    Example:
        Then User sees Today new added element
        
    Migration Notes:
        - Original lines 84-87: get text, compare with assertEquals
        - Assert.assertEquals(actualTable, expectedTable) on line 87
        - Converted to Python assert with descriptive error message
        - Expected text 'Today' preserved from original
    """
    logger.info("Step: User sees Today new added element")
    
    notes_page = NotesPage(context.driver)
    
    # Get actual text from today table element
    logger.debug("Retrieving text from today_table element")
    actual_table_text = notes_page.today_table.text
    
    # Expected text matches original Java implementation
    expected_table_text = "Today"
    
    logger.debug(f"Actual table text: '{actual_table_text}', Expected: '{expected_table_text}'")
    
    # Assert table text matches with descriptive error
    assert actual_table_text == expected_table_text, (
        f"Today table text verification failed. "
        f"Expected: '{expected_table_text}', Actual: '{actual_table_text}'"
    )
    
    logger.info("Successfully verified Today table contains expected element")
