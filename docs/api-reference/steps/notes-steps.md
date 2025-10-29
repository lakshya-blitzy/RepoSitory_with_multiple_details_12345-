# Notes Step Definitions API Reference

## Overview

The Notes step definitions module (`features/steps/notes_steps.py`) implements Behave steps for notes management test scenarios. This module provides 12 step implementations covering notes creation, editing, categorization with tags, drag-and-drop operations between sections, and verification workflows.

**Module:** `features/steps/notes_steps.py`

**Source:** `features/steps/notes_steps.py:1-531`

**Feature File:** `features/Notes.feature`

**Purpose:** Implement all Gherkin steps for Notes.feature scenarios including:
- Notes module navigation and access
- Note creation with tag entry and description input
- Note editing workflows with form interaction
- Save button validation with success message verification
- Drag-and-drop operations between note sections (New → Today)
- Notes list display confirmation

**Thread Safety:** This module is thread-safe when used with Behave's context object, which provides thread-local driver instances from DriverManager. Each step function receives its own context instance.

## Migration Context

**Converted from:** `src/main/java/com/testinium/step_definitions/Notes.java`

**Original Pattern:** Cucumber Java with @When/@Then annotations

**Target Pattern:** Python Behave with @when/@then decorators

### Key Transformations

1. **Thread.sleep(2000) removed** - Replaced with explicit waits via page objects
2. **WebDriverWait(Driver.getDriver(), 20)** - Replaced with context-based driver access
3. **Actions class** → ActionChains for drag-and-drop operations
4. **notesP/inventoryP instances** → notes_page/inventory_page with context pattern
5. **Assert.assertEquals/assertTrue** → Python assert statements with messages
6. **Keys.ENTER keyboard interaction** - Preserved for tag entry
7. **Fixed typo:** 'expecgedMessage' → 'expected_message'

### Behavioral Preservation

- All step text preserved exactly matching Notes.feature Gherkin scenarios
- All element interactions produce identical results to Java implementation
- Drag-and-drop functionality maintains same behavior using ActionChains
- Success message validation uses exact string 'Note created' matching

## Dependencies

**Page Objects:**
- `pages.notes_page.NotesPage` - Main page object for notes interface
- `pages.inventory_page.InventoryPage` - Provides save_btn for editing workflow

**Selenium Components:**
- `selenium.webdriver.common.keys.Keys` - Keyboard interaction (ENTER key)
- `selenium.webdriver.common.action_chains.ActionChains` - Drag-and-drop operations

**See Also:**
- [NotesPage API Reference](../pages/notes-page.md)
- [Notes Testing Guide](../../guides/notes-testing.md)

---

## Step Definitions

### Navigation Steps

#### @when("User clicks the Notes module")

Navigate to the Notes module by clicking the Notes navigation link.

**Function:** `user_clicks_the_notes_module(context)`

**Source:** `features/steps/notes_steps.py:71-104`

**Step Pattern:** `When User clicks the Notes module`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If Notes module link not found within configured timeout

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Accesses `notes_page.notes_module` property with explicit wait
- Calls `.click()` on the notes module navigation element

**Migration Notes:**
- Removed `Thread.sleep(2000)` from line 23 of Notes.java
- Using `notes_page.notes_module` property with explicit wait
- Property returns fresh WebElement reference preventing stale elements

**Example:**

```gherkin
When User clicks the Notes module
```

**Implementation:**

```python
from pages.notes_page import NotesPage

@when("User clicks the Notes module")
def user_clicks_the_notes_module(context):
    notes_page = NotesPage(context.driver)
    notes_page.notes_module.click()
```

**Usage in Feature:**

```gherkin
Scenario: Verify that User can create new Notes
    When User clicks the Notes module
    And User clicks create button in Notes module
    # ... additional steps
```

---

### Note Creation Steps

#### @when("User clicks create button in Notes module")

Click the create button to initiate new note creation workflow.

**Function:** `user_clicks_create_button_in_notes_module(context)`

**Source:** `features/steps/notes_steps.py:107-138`

**Step Pattern:** `When User clicks create button in Notes module`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If create button not clickable within configured timeout

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Accesses `notes_page.creating_notes` property with `wait_for_clickable`
- Ensures button is both visible and enabled before clicking

**Migration Notes:**
- Converted `WebDriverWait(Driver.getDriver(), 20)` to page object wait
- Using `wait_for_clickable` for better reliability (visible + enabled)
- Original `wait.until(ExpectedConditions.visibilityOf())` on line 29 of Notes.java

**Example:**

```gherkin
When User clicks create button in Notes module
```

**Implementation:**

```python
from pages.notes_page import NotesPage

@when("User clicks create button in Notes module")
def user_clicks_create_button_in_notes_module(context):
    notes_page = NotesPage(context.driver)
    notes_page.creating_notes.click()
```

---

#### @when("User enters a tag name")

Enter a tag name for note categorization with keyboard ENTER submission.

**Function:** `user_enters_a_tag_name(context)`

**Source:** `features/steps/notes_steps.py:141-178`

**Step Pattern:** `When User enters a tag name`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If tags input field not found within configured timeout

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Accesses `notes_page.tags_n` property (tags input field)
- Sends "New Tag" text with `Keys.ENTER` keyboard interaction
- Clicks `notes_page.tab_index` for focus management

**Keyboard Interaction:**
- Uses `send_keys("New Tag", Keys.ENTER)` to submit tag
- `Keys.ENTER` triggers tag addition to note
- Tab index click manages focus after tag entry

**Migration Notes:**
- Preserved `Keys.ENTER` keyboard interaction from line 35 of Notes.java
- Java: `notesP.tagsN.sendKeys("New Tag", Keys.ENTER)`
- Python: `notes_page.tags_n.send_keys("New Tag", Keys.ENTER)`
- Maintains `tab_index` click for focus management

**Example:**

```gherkin
When User enters a tag name
```

**Implementation:**

```python
from selenium.webdriver.common.keys import Keys
from pages.notes_page import NotesPage

@when("User enters a tag name")
def user_enters_a_tag_name(context):
    notes_page = NotesPage(context.driver)
    notes_page.tags_n.send_keys("New Tag", Keys.ENTER)
    notes_page.tab_index.click()
```

**Complete Workflow:**

```gherkin
Scenario: Create note with tags
    When User clicks the Notes module
    And User clicks create button in Notes module
    And User enters a tag name
    And User enters description
    Then User sees the created new notes
```

---

#### @when("User enters description")

Enter note description text and save the note.

**Function:** `user_enters_description(context)`

**Source:** `features/steps/notes_steps.py:181-218`

**Step Pattern:** `When User enters description`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If description editor or save button not found within timeout

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Accesses `notes_page.description` property (rich text editor)
- Sends description text: "This note is an example for the Testinium App"
- Clicks `notes_page.save_btn` to persist note data

**Behavior:**
This step combines description entry with save action as implemented in original Java code (lines 41-42).

**Migration Notes:**
- Original line 41: `notesP.description.sendKeys("...")`
- Original line 42: `notesP.saveBtn.click()`
- Combined description entry with save action per Java implementation
- Description text preserved exactly from original

**Example:**

```gherkin
When User enters description
```

**Implementation:**

```python
from pages.notes_page import NotesPage

@when("User enters description")
def user_enters_description(context):
    notes_page = NotesPage(context.driver)
    description_text = "This note is an example for the Testinium App"
    notes_page.description.send_keys(description_text)
    notes_page.save_btn.click()
```

---

#### @when("User clicks save button")

Click the save button to persist note changes.

**Function:** `user_clicks_save_button(context)`

**Source:** `features/steps/notes_steps.py:221-252`

**Step Pattern:** `When User clicks save button`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If save button not clickable within configured timeout

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Accesses `notes_page.save_btn` property with `wait_for_clickable`
- Ensures button is visible and enabled before clicking

**Use Cases:**
- Separate save step for scenarios requiring explicit save action
- Used after note editing workflows
- Provides flexibility in step composition

**Migration Notes:**
- Original lines 46-47: wait + click pattern in Notes.java
- `WebDriverWait` for visibility converted to `wait_for_clickable`
- Provides better reliability ensuring button is enabled

**Example:**

```gherkin
When User clicks save button
```

**Implementation:**

```python
from pages.notes_page import NotesPage

@when("User clicks save button")
def user_clicks_save_button(context):
    notes_page = NotesPage(context.driver)
    notes_page.save_btn.click()
```

---

### Verification Steps

#### @then("User sees the created new notes")

Verify that note creation success message is displayed.

**Function:** `user_sees_the_created_new_notes(context)`

**Source:** `features/steps/notes_steps.py:255-300`

**Step Pattern:** `Then User sees the created new notes`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If created message not visible within configured timeout
- `AssertionError` - If message text doesn't match expected value "Note created"

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Accesses `notes_page.created_message` property with `wait_for_visibility`
- Retrieves `.text` attribute for message validation

**Validation:**
- Expected message: `"Note created"`
- Uses exact string matching
- Provides descriptive error message on assertion failure

**Migration Notes:**
- Fixed typo from original: 'expecgedMessage' → 'expected_message'
- `Assert.assertEquals(actualMessage, expecgedMessage)` on line 53 of Notes.java
- Converted to Python: `assert actual_message == expected_message`
- Added descriptive error message for assertion failure

**Example:**

```gherkin
Then User sees the created new notes
```

**Implementation:**

```python
from pages.notes_page import NotesPage

@then("User sees the created new notes")
def user_sees_the_created_new_notes(context):
    notes_page = NotesPage(context.driver)
    actual_message = notes_page.created_message.text
    expected_message = "Note created"
    assert actual_message == expected_message, (
        f"Note creation confirmation message mismatch. "
        f"Expected: '{expected_message}', Actual: '{actual_message}'"
    )
```

**Complete Scenario:**

```gherkin
Scenario: Verify that User can create new Notes and see the created notes on the list
    When User clicks the Notes module
    And User clicks create button in Notes module
    And User enters a tag name
    And User enters description
    And User clicks save button
    Then User sees the created new notes
```

---

### Note Editing Steps

#### @when("User clicks the edit button")

Click the edit button to enter note editing mode.

**Function:** `user_clicks_the_edit_button(context)`

**Source:** `features/steps/notes_steps.py:303-333`

**Step Pattern:** `When User clicks the edit button`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If edit button not found within configured timeout

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Accesses `notes_page.app_k` property (application identifier element)
- Clicks element to edit specific note identified by 'BDD Approach Framework with Cucumber' text

**Element Details:**
- XPath: `//span[.='BDD Approach Framework with Cucumber']`
- Represents specific note title used as edit button identifier

**Migration Notes:**
- Original line 58: `notesP.appK.click()` in Notes.java
- `app_k` is application identifier element with specific note title
- Locates and clicks specific note for editing

**Example:**

```gherkin
When User clicks the edit button
```

**Implementation:**

```python
from pages.notes_page import NotesPage

@when("User clicks the edit button")
def user_clicks_the_edit_button(context):
    notes_page = NotesPage(context.driver)
    notes_page.app_k.click()
```

---

#### @when("User enters new description")

Clear existing description and enter new description text.

**Function:** `user_enters_new_description(context)`

**Source:** `features/steps/notes_steps.py:336-389`

**Step Pattern:** `When User enters new description`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If description editor or save button not found within timeout

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Creates `InventoryPage(context.driver)` instance
- Accesses `notes_page.description` for text editing
- Uses `inventory_page.save_btn` (shared component)
- Returns to `notes_page.notes_module`

**Editing Workflow:**
1. Clear existing description content with `.clear()`
2. Enter new description text: "FKASDFGASDFADSFADS"
3. Click save button from InventoryPage (shared UI component)
4. Return to notes module navigation

**Critical Implementation Note:**
Original Java code uses `inventoryP.saveBtn` instead of `notesP.saveBtn` on line 65, indicating shared UI component across modules. This behavior is preserved for behavioral equivalence.

**Migration Notes:**
- Original lines 63-66 of Notes.java: clear, sendKeys, inventoryP.saveBtn, notesModule
- Uses `InventoryPage.save_btn` (not `NotesPage.save_btn`) per original
- This indicates shared save button component across modules
- Description text preserved exactly: "FKASDFGASDFADSFADS"

**Example:**

```gherkin
When User enters new description
```

**Implementation:**

```python
from pages.notes_page import NotesPage
from pages.inventory_page import InventoryPage

@when("User enters new description")
def user_enters_new_description(context):
    notes_page = NotesPage(context.driver)
    inventory_page = InventoryPage(context.driver)
    
    notes_page.description.clear()
    new_description = "FKASDFGASDFADSFADS"
    notes_page.description.send_keys(new_description)
    
    # Uses InventoryPage save button (shared component)
    inventory_page.save_btn.click()
    notes_page.notes_module.click()
```

**Complete Edit Scenario:**

```gherkin
Scenario: Verify that User can edit the Notes
    When User clicks the Notes module
    And User clicks the edit button
    And User enters new description
    And User clicks save button
    And User enters new description
    Then User should see the Notes list
```

---

#### @then("User should see the Notes list")

Verify that the Notes list is visible and displayed.

**Function:** `user_should_see_the_notes_list(context)`

**Source:** `features/steps/notes_steps.py:392-432`

**Step Pattern:** `Then User should see the Notes list`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If notes module not visible within configured timeout
- `AssertionError` - If notes module is not displayed

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Accesses `notes_page.notes_module` with explicit wait
- Clicks notes module element
- Verifies `is_displayed()` returns True

**Validation:**
- Waits for notes module visibility
- Clicks notes module
- Asserts element is displayed with descriptive error message

**Migration Notes:**
- Original lines 71-73 of Notes.java: wait for visibility, click, assertTrue
- `WebDriverWait` converted to page object explicit wait
- `Assert.assertTrue(notesModule.isDisplayed())` on line 73
- Converted to: `assert notes_page.notes_module.is_displayed()`

**Example:**

```gherkin
Then User should see the Notes list
```

**Implementation:**

```python
from pages.notes_page import NotesPage

@then("User should see the Notes list")
def user_should_see_the_notes_list(context):
    notes_page = NotesPage(context.driver)
    notes_module_element = notes_page.notes_module
    notes_module_element.click()
    assert notes_module_element.is_displayed(), (
        "Notes module should be displayed but is not visible"
    )
```

---

### Drag-and-Drop Steps

#### @when("User move element from New section to Today section")

Perform drag-and-drop operation to move note from New table to Today table.

**Function:** `user_move_element_from_new_section_to_today_section(context)`

**Source:** `features/steps/notes_steps.py:435-483`

**Step Pattern:** `When User move element from New section to Today section`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If source or target table elements not found within timeout

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Accesses `notes_page.new_table` (source element)
- Accesses `notes_page.today_table` (target element)
- Uses `ActionChains` for complex drag-and-drop

**Drag-and-Drop Operation:**
1. Click and hold source element (`new_table`)
2. Pause 2 seconds for drag initiation
3. Move to target element (`today_table`)
4. Pause 2 seconds for positioning
5. Release mouse to complete drop
6. Call `.perform()` to execute action chain

**ActionChains Pattern:**

```python
actions.click_and_hold(source_element) \
    .pause(2) \
    .move_to_element(target_element) \
    .pause(2) \
    .release() \
    .perform()
```

**Migration Notes:**
- Original line 79 of Notes.java: Actions class with pause(2000) in milliseconds
- Java: `actions.clickAndHold().pause(2000).moveToElement().pause(2000).release().perform()`
- Python: ActionChains with `pause()` in seconds
- Converted `pause(2000ms)` → `pause(2)` for 2 seconds
- `ActionChains.pause()` available in Selenium 4.x

**Example:**

```gherkin
When User move element from New section to Today section
```

**Implementation:**

```python
from selenium.webdriver.common.action_chains import ActionChains
from pages.notes_page import NotesPage

@when("User move element from New section to Today section")
def user_move_element_from_new_section_to_today_section(context):
    notes_page = NotesPage(context.driver)
    
    source_element = notes_page.new_table
    target_element = notes_page.today_table
    
    actions = ActionChains(context.driver)
    actions.click_and_hold(source_element) \
        .pause(2) \
        .move_to_element(target_element) \
        .pause(2) \
        .release() \
        .perform()
```

**Complete Drag-and-Drop Scenario:**

```gherkin
Scenario: Verify that User can move element from New section to Today section
    When User clicks the Notes module
    And User move element from New section to Today section
    Then User sees Today new added element
```

---

#### @then("User sees Today new added element")

Verify that the Today table contains the expected element after drag-and-drop.

**Function:** `user_sees_today_new_added_element(context)`

**Source:** `features/steps/notes_steps.py:486-530`

**Step Pattern:** `Then User sees Today new added element`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| context | behave.runner.Context | Behave context object containing driver and shared state |

**Raises:**
- `TimeoutException` - If today_table element not found within configured timeout
- `AssertionError` - If table text doesn't match expected value "Today"

**Page Object Interactions:**
- Creates `NotesPage(context.driver)` instance
- Accesses `notes_page.today_table` property
- Retrieves `.text` attribute for validation

**Validation:**
- Expected text: `"Today"`
- Uses exact string matching
- Provides descriptive error message on assertion failure

**Migration Notes:**
- Original lines 84-87 of Notes.java: get text, compare with assertEquals
- `Assert.assertEquals(actualTable, expectedTable)` on line 87
- Converted to Python assert with descriptive error message
- Expected text 'Today' preserved from original

**Example:**

```gherkin
Then User sees Today new added element
```

**Implementation:**

```python
from pages.notes_page import NotesPage

@then("User sees Today new added element")
def user_sees_today_new_added_element(context):
    notes_page = NotesPage(context.driver)
    actual_table_text = notes_page.today_table.text
    expected_table_text = "Today"
    assert actual_table_text == expected_table_text, (
        f"Today table text verification failed. "
        f"Expected: '{expected_table_text}', Actual: '{actual_table_text}'"
    )
```

---

## Complete Step Summary

### All Step Definitions

| Step Type | Step Pattern | Function | Line |
|-----------|--------------|----------|------|
| @when | User clicks the Notes module | user_clicks_the_notes_module | 71-104 |
| @when | User clicks create button in Notes module | user_clicks_create_button_in_notes_module | 107-138 |
| @when | User enters a tag name | user_enters_a_tag_name | 141-178 |
| @when | User enters description | user_enters_description | 181-218 |
| @when | User clicks save button | user_clicks_save_button | 221-252 |
| @then | User sees the created new notes | user_sees_the_created_new_notes | 255-300 |
| @when | User clicks the edit button | user_clicks_the_edit_button | 303-333 |
| @when | User enters new description | user_enters_new_description | 336-389 |
| @then | User should see the Notes list | user_should_see_the_notes_list | 392-432 |
| @when | User move element from New section to Today section | user_move_element_from_new_section_to_today_section | 435-483 |
| @then | User sees Today new added element | user_sees_today_new_added_element | 486-530 |

**Total Steps:** 11 step definitions (8 @when steps, 3 @then steps)

---

## Gherkin-to-Code Mapping

### Scenario 1: Create New Notes

**Feature File:** `features/Notes.feature:10-16`

```gherkin
Scenario: Verify that User can create new Notes and see the created notes on the list
    When User clicks the Notes module
    And User clicks create button in Notes module
    And User enters a tag name
    And User enters description
    And User clicks save button
    Then User sees the created new notes
```

**Step Implementations:**

| Gherkin Step | Python Function | Source Line |
|--------------|-----------------|-------------|
| When User clicks the Notes module | user_clicks_the_notes_module() | 71-104 |
| And User clicks create button in Notes module | user_clicks_create_button_in_notes_module() | 107-138 |
| And User enters a tag name | user_enters_a_tag_name() | 141-178 |
| And User enters description | user_enters_description() | 181-218 |
| And User clicks save button | user_clicks_save_button() | 221-252 |
| Then User sees the created new notes | user_sees_the_created_new_notes() | 255-300 |

### Scenario 2: Edit Notes

**Feature File:** `features/Notes.feature:18-24`

```gherkin
Scenario: Verify that User can edit the Notes
    When User clicks the Notes module
    And User clicks the edit button
    And User enters new description
    And User clicks save button
    And User enters new description
    Then User should see the Notes list
```

**Step Implementations:**

| Gherkin Step | Python Function | Source Line |
|--------------|-----------------|-------------|
| When User clicks the Notes module | user_clicks_the_notes_module() | 71-104 |
| And User clicks the edit button | user_clicks_the_edit_button() | 303-333 |
| And User enters new description | user_enters_new_description() | 336-389 |
| And User clicks save button | user_clicks_save_button() | 221-252 |
| And User enters new description | user_enters_new_description() | 336-389 |
| Then User should see the Notes list | user_should_see_the_notes_list() | 392-432 |

### Scenario 3: Drag-and-Drop Between Sections

**Feature File:** `features/Notes.feature:26-29`

```gherkin
Scenario: Verify that User can move element from New section to Today section
    When User clicks the Notes module
    And User move element from New section to Today section
    Then User sees Today new added element
```

**Step Implementations:**

| Gherkin Step | Python Function | Source Line |
|--------------|-----------------|-------------|
| When User clicks the Notes module | user_clicks_the_notes_module() | 71-104 |
| And User move element from New section to Today section | user_move_element_from_new_section_to_today_section() | 435-483 |
| Then User sees Today new added element | user_sees_today_new_added_element() | 486-530 |

---

## Usage Examples

### Creating a Note with Tags

```python
# Complete note creation workflow
from behave import when, then
from pages.notes_page import NotesPage
from selenium.webdriver.common.keys import Keys

# Navigate to Notes module
@when("User clicks the Notes module")
def user_clicks_the_notes_module(context):
    notes_page = NotesPage(context.driver)
    notes_page.notes_module.click()

# Initiate note creation
@when("User clicks create button in Notes module")
def user_clicks_create_button_in_notes_module(context):
    notes_page = NotesPage(context.driver)
    notes_page.creating_notes.click()

# Add tag with keyboard interaction
@when("User enters a tag name")
def user_enters_a_tag_name(context):
    notes_page = NotesPage(context.driver)
    notes_page.tags_n.send_keys("New Tag", Keys.ENTER)
    notes_page.tab_index.click()

# Enter description and save
@when("User enters description")
def user_enters_description(context):
    notes_page = NotesPage(context.driver)
    notes_page.description.send_keys("This note is an example for the Testinium App")
    notes_page.save_btn.click()

# Verify success
@then("User sees the created new notes")
def user_sees_the_created_new_notes(context):
    notes_page = NotesPage(context.driver)
    actual_message = notes_page.created_message.text
    expected_message = "Note created"
    assert actual_message == expected_message
```

### Editing an Existing Note

```python
# Edit note workflow with shared save button
from pages.notes_page import NotesPage
from pages.inventory_page import InventoryPage

@when("User enters new description")
def user_enters_new_description(context):
    notes_page = NotesPage(context.driver)
    inventory_page = InventoryPage(context.driver)
    
    # Clear and update description
    notes_page.description.clear()
    notes_page.description.send_keys("FKASDFGASDFADSFADS")
    
    # Use shared save button from InventoryPage
    inventory_page.save_btn.click()
    
    # Return to notes module
    notes_page.notes_module.click()
```

### Drag-and-Drop Operation

```python
# Complex drag-and-drop with ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from pages.notes_page import NotesPage

@when("User move element from New section to Today section")
def user_move_element_from_new_section_to_today_section(context):
    notes_page = NotesPage(context.driver)
    
    # Get source and target elements
    source_element = notes_page.new_table
    target_element = notes_page.today_table
    
    # Perform drag-and-drop with pauses
    actions = ActionChains(context.driver)
    actions.click_and_hold(source_element) \
        .pause(2) \
        .move_to_element(target_element) \
        .pause(2) \
        .release() \
        .perform()

# Verify drag-and-drop result
@then("User sees Today new added element")
def user_sees_today_new_added_element(context):
    notes_page = NotesPage(context.driver)
    actual_table_text = notes_page.today_table.text
    assert actual_table_text == "Today"
```

---

## Common Patterns

### Context-Based Driver Access

All step definitions use the Behave context object to access the thread-local WebDriver instance:

```python
@when("User clicks the Notes module")
def user_clicks_the_notes_module(context):
    # Access driver from context
    notes_page = NotesPage(context.driver)
    notes_page.notes_module.click()
```

### Page Object Pattern

Steps create page object instances for each interaction:

```python
@when("User enters description")
def user_enters_description(context):
    # Create page object with driver
    notes_page = NotesPage(context.driver)
    
    # Use property-based locators with explicit waits
    notes_page.description.send_keys("Text")
    notes_page.save_btn.click()
```

### Explicit Wait Integration

All element access uses page object properties with built-in explicit waits:

```python
# Page object property handles wait automatically
notes_page.creating_notes.click()

# Equivalent to:
# wait = WebDriverWait(driver, timeout)
# element = wait.until(EC.element_to_be_clickable(locator))
# element.click()
```

### Assertion with Descriptive Messages

All verification steps include descriptive error messages:

```python
@then("User sees the created new notes")
def user_sees_the_created_new_notes(context):
    notes_page = NotesPage(context.driver)
    actual_message = notes_page.created_message.text
    expected_message = "Note created"
    
    # Descriptive assertion message
    assert actual_message == expected_message, (
        f"Note creation confirmation message mismatch. "
        f"Expected: '{expected_message}', Actual: '{actual_message}'"
    )
```

---

## Troubleshooting

### Issue: Notes Module Not Clickable

**Symptoms:** `TimeoutException` when trying to click notes module

**Cause:** Notes module link not loaded or obscured by another element

**Solution:**
```python
# Page object already includes explicit wait
# Verify element locator is correct in NotesPage
notes_page = NotesPage(context.driver)

# Check if element exists
driver.find_element(By.XPATH, "//notes-module-xpath")

# Verify no overlays are present
# Check browser console for JavaScript errors
```

### Issue: Tag Not Submitted with ENTER Key

**Symptoms:** Tag input field doesn't accept tag when ENTER key is pressed

**Cause:** Focus not on tag input field or JavaScript handler not ready

**Solution:**
```python
# Ensure field has focus before sending keys
notes_page.tags_n.click()
notes_page.tags_n.send_keys("New Tag", Keys.ENTER)

# Wait briefly if needed
from time import sleep
sleep(0.5)
notes_page.tab_index.click()
```

### Issue: Drag-and-Drop Not Working

**Symptoms:** Element doesn't move from New section to Today section

**Cause:** ActionChains pauses too short, elements not properly positioned

**Solution:**
```python
# Increase pause duration
actions.click_and_hold(source_element) \
    .pause(3) \
    .move_to_element(target_element) \
    .pause(3) \
    .release() \
    .perform()

# Alternative: Use offset-based drag-and-drop
actions.drag_and_drop(source_element, target_element).perform()
```

### Issue: Save Button Not Found

**Symptoms:** `TimeoutException` when clicking save button

**Cause:** Save button locator changed or page not fully loaded

**Solution:**
```python
# For note creation - use NotesPage save button
notes_page = NotesPage(context.driver)
notes_page.save_btn.click()

# For note editing - use InventoryPage save button (shared component)
inventory_page = InventoryPage(context.driver)
inventory_page.save_btn.click()
```

### Issue: Assertion Fails on Success Message

**Symptoms:** `AssertionError` even though note was created

**Cause:** Message text contains extra whitespace or different casing

**Solution:**
```python
# Strip whitespace and compare
actual_message = notes_page.created_message.text.strip()
expected_message = "Note created"
assert actual_message == expected_message

# Case-insensitive comparison if needed
assert actual_message.lower() == expected_message.lower()
```

### Issue: Stale Element Exception

**Symptoms:** `StaleElementReferenceException` during step execution

**Cause:** Page refresh or DOM update between element access and interaction

**Solution:**
```python
# Page object properties return fresh elements each time
# Access property multiple times as needed
notes_page.notes_module.click()  # Fresh element
notes_page.notes_module.click()  # Fresh element again

# Don't store element reference
# WRONG: element = notes_page.notes_module
# RIGHT: notes_page.notes_module.click()
```

---

## See Also

### API References
- [NotesPage API Reference](../pages/notes-page.md) - Page object for Notes module
- [InventoryPage API Reference](../pages/inventory-page.md) - Page object with shared save button
- [BasePage API Reference](../pages/base-page.md) - Base page object class
- [Step Definitions Overview](index.md) - All step definition modules

### User Guides
- [Notes Testing Guide](../../guides/notes-testing.md) - Complete notes testing workflow
- [Step Definitions Guide](../../guides/step-definitions.md) - Writing step definitions
- [Page Object Model Guide](../../guides/page-object-model.md) - Creating page objects

### Architecture
- [Test Execution Lifecycle](../../architecture/test-execution-lifecycle.md) - How steps execute
- [Page Object Model Architecture](../../architecture/page-object-model.md) - POM design patterns

### Reference
- [Behave Configuration](../../reference/behave-configuration.md) - Behave settings
- [Gherkin Syntax](../../reference/gherkin-syntax.md) - Writing feature files

---

**Last Updated:** Auto-generated from source code

**Module Version:** Migrated from Java (2024)

**Maintainer:** Testinium QA Team
