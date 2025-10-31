# CalendarPage API Reference

## Overview

The `CalendarPage` class provides a Page Object Model implementation for the Calendar/Meetings module in the Testinium application. It encapsulates all calendar interface interactions including navigation, view controls, date selection, and meeting/note management functionality.

**Module:** `pages.calendar_page`  
**Class:** `CalendarPage`  
**Inherits From:** [`BasePage`](base-page.md)  
**Source:** `pages/calendar_page.py`

## Migration Context

This page object was converted from the Java implementation using PageFactory patterns to Python property-based locators.

- **Java Source:** `src/main/java/com/testinium/pages/CalendarP.java`
- **Migration Pattern:** `@FindBy` annotations → Private locator tuples + `@property` methods
- **Pattern Change:** Public WebElement fields → Property-based element access

## Class Definition

```python
class CalendarPage(BasePage):
    """
    Page Object for Calendar/Meetings module with meeting management capabilities.
    
    Inherits from BasePage to leverage explicit wait strategies and prevent stale
    element references through property-based element access.
    """
```

**Thread Safety:** Thread-safe when each thread has its own WebDriver instance (via `DriverManager`)

## Initialization

### `__init__(driver: WebDriver) -> None`

Initialize CalendarPage with a WebDriver instance.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| driver | WebDriver | Yes | Selenium WebDriver instance for browser automation. Expected to be thread-local instance from DriverManager |

**Example:**

```python
from utilities.driver_manager import DriverManager
from pages.calendar_page import CalendarPage

# Get thread-local driver instance
driver = DriverManager.get_driver()

# Initialize page object
calendar_page = CalendarPage(driver)
```

**Source:** `pages/calendar_page.py:167-183`

## Element Properties

All properties return fresh `WebElement` references on each access to prevent stale element exceptions. Properties use `BasePage` wait methods to ensure elements are available before returning.

### Element Categories

- **Navigation:** `calendar_button`
- **View Controls:** `day`, `week`, `month`
- **Calendar Display:** `calendar_module`, `day_calendar`, `month_and_year_calendar`
- **Date Information:** `date_actual`, `date_box`
- **Note Management:** `create_note`, `summary_box`, `get_note`, `select_note`, `created_note`
- **Action Buttons:** `create_button`, `edit_button`, `save_button`
- **Form Fields:** `edit_text`, `tags_checkbox`
- **Modals:** `created_modele`

---

### Navigation Elements

#### `title`

Page title element containing 'Meetings - Odoo'.

**Returns:** `WebElement` - Title element when present in DOM

**Raises:** `TimeoutException` - If title not found within default timeout

**Locator Strategy:** XPath  
**Locator Value:** `//title[.='Meetings - Odoo']`

**Source:** `pages/calendar_page.py:192-202`

---

#### `calendar_button`

Calendar navigation link for accessing the calendar module.

Use this element to navigate to the calendar/meetings page from other modules.

**Returns:** `WebElement` - Clickable calendar navigation link

**Raises:** `TimeoutException` - If calendar button not clickable within timeout

**Locator Strategy:** Partial Link Text  
**Locator Value:** `"Calendar"`

**Example:**

```python
# Navigate to calendar module
calendar_page.calendar_button.click()
```

**Source:** `pages/calendar_page.py:205-220`

---

### View Control Elements

#### `day`

Day view button to switch calendar to daily view.

**Returns:** `WebElement` - Clickable 'Day' button

**Raises:** `TimeoutException` - If day button not clickable within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//button[.='Day']`

**Example:**

```python
# Switch to day view
calendar_page.day.click()
```

**Source:** `pages/calendar_page.py:238-252`

---

#### `week`

Week view button to switch calendar to weekly view.

**Returns:** `WebElement` - Clickable 'Week' button

**Raises:** `TimeoutException` - If week button not clickable within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//button[.='Week']`

**Example:**

```python
# Switch to week view
calendar_page.week.click()
```

**Source:** `pages/calendar_page.py:254-268`

---

#### `month`

Month view button to switch calendar to monthly view.

**Returns:** `WebElement` - Clickable 'Month' button

**Raises:** `TimeoutException` - If month button not clickable within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//button[.='Month']`

**Example:**

```python
# Switch to month view
calendar_page.month.click()
```

**Source:** `pages/calendar_page.py:270-284`

---

### Calendar Display Elements

#### `calendar_module`

Main calendar container element.

This element contains the entire calendar interface including view controls, date navigation, and calendar grid.

**Returns:** `WebElement` - Calendar container when visible

**Raises:** `TimeoutException` - If calendar module not visible within timeout

**Locator Strategy:** Class Name  
**Locator Value:** `"o_calendar_container"`

**Source:** `pages/calendar_page.py:222-236`

---

#### `day_calendar`

Current day highlight element in calendar view.

This element represents the currently selected or highlighted day in the calendar interface, typically styled to stand out from other dates.

**Returns:** `WebElement` - Highlighted day element

**Raises:** `TimeoutException` - If day calendar element not found within timeout

**Locator Strategy:** Class Name  
**Locator Value:** `"ui-state-highlight"`

**Source:** `pages/calendar_page.py:286-300`

---

#### `month_and_year_calendar`

Current date cell in month/year calendar view.

Represents today's date cell with special styling in the calendar grid. Used for date selection and current date verification.

**Returns:** `WebElement` - Today's date cell element

**Raises:** `TimeoutException` - If date cell not found within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//td[@class=' ui-datepicker-days-cell-over  ui-datepicker-current-day ui-datepicker-today']`

**Source:** `pages/calendar_page.py:302-316`

---

### Date Information Elements

#### `date_actual`

Currently displayed date information in control panel.

Shows the current date context (e.g., "Week 45, 2024" or "November 2024") depending on the active calendar view (day/week/month).

**Returns:** `WebElement` - Date display element in control panel

**Raises:** `TimeoutException` - If date element not found within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//div[@class='o_control_panel']/ol/li`

**Example:**

```python
# Get and verify displayed date
actual_date = calendar_page.date_actual.text
assert "2024" in actual_date
```

**Source:** `pages/calendar_page.py:318-336`

---

#### `date_box`

Specific date cell in calendar grid for meeting creation.

⚠️ **WARNING - TECHNICAL DEBT:** This locator uses a brittle index-based XPath selector `[29]` which may break if the calendar view changes or DOM structure is modified. This is preserved for behavioral equivalence with the Java implementation.

Consider using date-based attributes (e.g., `data-date="2024-11-07"`) if the application provides them for more stable element identification.

**Returns:** `WebElement` - Date cell element at position [29]

**Raises:** 
- `TimeoutException` - If date box not found within timeout
- `NoSuchElementException` - If calendar structure changed and index invalid

**Locator Strategy:** XPath  
**Locator Value:** `(//td[@class='fc-widget-content'])[29]`

**Example:**

```python
# Click specific date to open meeting creation dialog
calendar_page.date_box.click()
```

**Source:** `pages/calendar_page.py:338-361`

---

### Note Management Elements

#### `create_note`

Modal header for note/meeting creation dialog.

This element appears when creating a new meeting or note. Its presence indicates the creation modal is displayed.

**Returns:** `WebElement` - Modal header element

**Raises:** `TimeoutException` - If create note modal not visible within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//div[@class='modal-header']`

**Example:**

```python
# Verify creation modal is displayed
assert calendar_page.create_note.is_displayed()
```

**Source:** `pages/calendar_page.py:363-380`

---

#### `summary_box`

Input field for meeting/note summary (name/title).

Primary input field where users enter the title or summary of a meeting or note.

**Returns:** `WebElement` - Summary input field

**Raises:** `TimeoutException` - If summary box not found within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//input[@name='name']`

**Example:**

```python
# Enter meeting title
calendar_page.summary_box.send_keys("Team Standup Meeting")
```

**Source:** `pages/calendar_page.py:382-398`

---

#### `get_note`

Note field element displaying meeting/note details.

⚠️ **WARNING - TECHNICAL DEBT - DUPLICATE LOCATOR:** This property shares the same XPath locator with `select_note`: `xpath='//div[@class="o_field_name o_field_type_char"]'`

If multiple note field elements exist, Selenium returns the first match. The distinction between `get_note` and `select_note` in the Java implementation (lines 52-53 and 73-74) is unclear with identical locators.

**RECOMMENDATION:** Use more specific locators or add unique attributes to distinguish different note field contexts in the application.

**Returns:** `WebElement` - Note field element (or first matching field)

**Raises:** `TimeoutException` - If note field not found within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//div[@class='o_field_name o_field_type_char']`

**Example:**

```python
# Read note text
note_text = calendar_page.get_note.text
```

**Source:** `pages/calendar_page.py:431-456`

---

#### `created_note`

Display element for created note/meeting name.

Shows the name/title of a successfully created meeting or note. Different from `get_note`/`select_note` by using className locator strategy.

**Returns:** `WebElement` - Created note display element

**Raises:** `TimeoutException` - If created note element not found within timeout

**Locator Strategy:** Class Name  
**Locator Value:** `"o_field_name"`

**Example:**

```python
# Verify meeting was created
assert "Team Meeting" in calendar_page.created_note.text
```

**Source:** `pages/calendar_page.py:458-475`

---

#### `select_note`

Note selection element for interacting with specific notes.

⚠️ **WARNING - TECHNICAL DEBT - DUPLICATE LOCATOR:** This property shares the same XPath locator with `get_note`: `xpath='//div[@class="o_field_name o_field_type_char"]'`

See `get_note` property documentation for full details on this duplication issue.

**Returns:** `WebElement` - Note selection element (or first matching field)

**Raises:** `TimeoutException` - If select note element not found within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//div[@class='o_field_name o_field_type_char']`

**Source:** `pages/calendar_page.py:587-604`

---

### Action Button Elements

#### `create_button`

Button to create/save a new meeting or note.

⚠️ **WARNING - TECHNICAL DEBT - DUPLICATE LOCATOR:** This property shares the same XPath locator with `edit_button`: `xpath='//button[@class="btn btn-sm btn-primary"]'`

If both create and edit buttons are present on the page simultaneously, Selenium may return the first matching element, which could be either button.

This is preserved for behavioral equivalence with Java implementation (CalendarP.java lines 49-50 and 58-59 both use identical locators).

**RECOMMENDATION:** Application should add unique identifiers:
- `data-testid="create-button"` and `data-testid="edit-button"`, OR
- Unique `id` attributes for each button

**Returns:** `WebElement` - Create button (or first matching primary button)

**Raises:** `TimeoutException` - If create button not clickable within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//button[@class='btn btn-sm btn-primary']`

**Example:**

```python
# Create a new meeting
calendar_page.summary_box.send_keys("Meeting")
calendar_page.create_button.click()
```

**Source:** `pages/calendar_page.py:400-429`

---

#### `edit_button`

Button to edit an existing meeting or note.

⚠️ **WARNING - TECHNICAL DEBT - DUPLICATE LOCATOR:** This property shares the same XPath locator with `create_button`: `xpath='//button[@class="btn btn-sm btn-primary"]'`

See `create_button` property documentation for full details on this issue. When both buttons present, Selenium may return either button (first match).

This duplicate is preserved from Java implementation (CalendarP.java lines 49-50 for createButton and 58-59 for editButton use identical XPath).

**Returns:** `WebElement` - Edit button (or first matching primary button)

**Raises:** `TimeoutException` - If edit button not clickable within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//button[@class='btn btn-sm btn-primary']`

**Example:**

```python
# Edit existing meeting
calendar_page.edit_button.click()
calendar_page.edit_text.clear()
calendar_page.edit_text.send_keys("Updated Meeting Title")
```

**Source:** `pages/calendar_page.py:477-503`

---

#### `save_button`

Save button to persist meeting/note changes.

Finalizes edits or creation of meetings/notes by saving changes to the system.

**Returns:** `WebElement` - Clickable save button

**Raises:** `TimeoutException` - If save button not clickable within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//span[.='Save']`

**Example:**

```python
# Save changes
calendar_page.edit_text.send_keys("Updated")
calendar_page.save_button.click()
```

**Source:** `pages/calendar_page.py:568-585`

---

### Form Field Elements

#### `edit_text`

Text input field for editing meeting/note content.

This field appears in the edit mode of a meeting or note, allowing users to modify the meeting title or description.

⚠️ **Note:** Uses ID locator `'o_field_input_46'` which may be dynamically generated. If the application uses dynamic IDs, this locator may become unreliable.

**Returns:** `WebElement` - Edit text input field

**Raises:** `TimeoutException` - If edit text field not found within timeout

**Locator Strategy:** ID  
**Locator Value:** `"o_field_input_46"`

**Example:**

```python
# Update meeting content
calendar_page.edit_text.clear()
calendar_page.edit_text.send_keys("Updated content")
```

**Source:** `pages/calendar_page.py:505-526`

---

#### `tags_checkbox`

Checkbox or input for selecting/managing meeting tags.

Allows users to categorize meetings with tags for organization and filtering.

⚠️ **Note:** Uses ID locator `'o_field_input_59'` which may be dynamically generated. If the application uses dynamic IDs, this locator may become unreliable.

**Returns:** `WebElement` - Tags checkbox/input element

**Raises:** `TimeoutException` - If tags checkbox not found within timeout

**Locator Strategy:** ID  
**Locator Value:** `"o_field_input_59"`

**Example:**

```python
# Select tags for meeting
calendar_page.tags_checkbox.click()
```

**Source:** `pages/calendar_page.py:547-566`

---

### Modal Elements

#### `created_modele`

Modal content container for created meeting/note.

This element represents the modal dialog content area that displays after creating or opening a meeting/note.

**Returns:** `WebElement` - Modal content container

**Raises:** `TimeoutException` - If modal content not visible within timeout

**Locator Strategy:** XPath  
**Locator Value:** `//div[@class='modal-content']`

**Example:**

```python
# Verify modal is displayed
assert calendar_page.created_modele.is_displayed()
```

**Source:** `pages/calendar_page.py:528-545`

---

## Technical Debt Documentation

The CalendarPage implementation contains several technical debt items inherited from the Java source code. These issues are documented here for future refactoring consideration.

### 1. Duplicate Locators - Create and Edit Buttons

**Issue:** Both `create_button` and `edit_button` properties use the identical XPath locator:
```xpath
//button[@class='btn btn-sm btn-primary']
```

**Impact:**
- When both buttons are present on the page, Selenium returns the first matching element
- Test automation cannot reliably distinguish between create and edit actions
- May cause test flakiness depending on DOM rendering order

**Root Cause:** Java source (CalendarP.java lines 49-50 and 58-59) defined both elements with identical `@FindBy` annotations

**Recommendation:**
- Add unique test identifiers to application code:
  - `<button class="btn btn-sm btn-primary" data-testid="create-button">Create</button>`
  - `<button class="btn btn-sm btn-primary" data-testid="edit-button">Edit</button>`
- Update locators to use unique identifiers: `By.CSS_SELECTOR, "[data-testid='create-button']"`

**Source:** `pages/calendar_page.py:137-142, 149-150`

---

### 2. Duplicate Locators - Note Field Elements

**Issue:** Both `get_note` and `select_note` properties use the identical XPath locator:
```xpath
//div[@class='o_field_name o_field_type_char']
```

**Impact:**
- Cannot distinguish between different note field contexts
- Both properties return the same element (first match)
- Unclear semantic difference between "get_note" and "select_note"

**Root Cause:** Java source (CalendarP.java lines 52-53 and 73-74) defined both with identical `@FindBy` annotations

**Recommendation:**
- Identify the semantic difference between these two note contexts in the application
- Add unique identifiers or use more specific ancestor/sibling relationships in XPath
- Consider consolidating into a single property if they serve the same purpose

**Source:** `pages/calendar_page.py:144-146, 160-161`

---

### 3. Brittle Index-Based XPath - Date Box

**Issue:** The `date_box` property uses positional index in XPath:
```xpath
(//td[@class='fc-widget-content'])[29]
```

**Impact:**
- Locator breaks if calendar view changes (different week displayed)
- Fragile against DOM structure modifications (cells added/removed)
- Screen resolution changes may affect rendered cells and break index
- Test reliability depends on consistent calendar state

**Root Cause:** Java source (CalendarP.java lines 40-41) used hardcoded positional index

**Recommendation:**
- Use date-based attributes if available: `//td[@data-date='2024-11-07']`
- Calculate date cell dynamically based on desired date
- Use relative positioning from known anchor elements (e.g., current date cell)

**Mitigation:** Tests using `date_box` should ensure calendar is in expected state before interaction

**Source:** `pages/calendar_page.py:127-131`

---

### 4. Potentially Dynamic ID Attributes

**Issue:** Two properties rely on numeric ID attributes that may be dynamically generated:
- `edit_text`: `id="o_field_input_46"`
- `tags_checkbox`: `id="o_field_input_59"`

**Impact:**
- If IDs are session-dependent or dynamically generated, locators will fail
- Tests may become unreliable across different environments or sessions

**Investigation Needed:** Verify if these IDs are stable across:
- Multiple test runs
- Different user sessions
- Different environments (dev/staging/production)

**Recommendation:** If IDs are dynamic, switch to:
- Name attributes if available
- Data attributes added for testing purposes
- XPath using label text or field position

**Source:** `pages/calendar_page.py:153, 155`

---

## Complete Usage Example

This example demonstrates a complete calendar workflow including navigation, view switching, meeting creation, and verification.

```python
from selenium import webdriver
from utilities.driver_manager import DriverManager
from pages.calendar_page import CalendarPage

# Initialize driver and page object
driver = DriverManager.get_driver()
calendar_page = CalendarPage(driver)

# Navigate to calendar module
calendar_page.calendar_button.click()

# Verify calendar module is displayed
assert calendar_page.calendar_module.is_displayed(), "Calendar module not displayed"

# Switch to day view
calendar_page.day.click()

# Verify current date is displayed
current_date = calendar_page.date_actual.text
print(f"Current calendar view: {current_date}")

# Create a new meeting
calendar_page.date_box.click()

# Wait for creation modal
assert calendar_page.create_note.is_displayed(), "Creation modal not displayed"

# Fill in meeting details
calendar_page.summary_box.send_keys("Team Standup Meeting")

# Save the meeting
calendar_page.create_button.click()

# Verify meeting was created
assert "Team Standup Meeting" in calendar_page.created_note.text

# Edit the meeting
calendar_page.edit_button.click()
calendar_page.edit_text.clear()
calendar_page.edit_text.send_keys("Daily Team Standup")

# Add tags
calendar_page.tags_checkbox.click()

# Save changes
calendar_page.save_button.click()

# Switch to week view to see the meeting
calendar_page.week.click()

# Switch to month view
calendar_page.month.click()

# Cleanup
DriverManager.quit_driver()
```

**Source:** Based on `pages/calendar_page.py:608-652`

---

## See Also

- [BasePage API Reference](base-page.md) - Parent class providing wait utilities
- [Calendar Testing Guide](../../guides/calendar-testing.md) - Feature-specific testing patterns
- [Page Object Model Guide](../../guides/page-object-model.md) - Creating page objects
- [Wait Strategies Guide](../../guides/wait-strategies.md) - Choosing appropriate wait methods

---

## Summary

The `CalendarPage` class provides comprehensive access to the Calendar/Meetings module with 21 element properties organized into:

- 1 navigation element
- 3 view control buttons
- 3 calendar display elements
- 2 date information elements
- 5 note management elements
- 3 action buttons
- 2 form fields
- 1 modal element
- 1 page title element

**Key Characteristics:**
- Property-based locator pattern prevents stale elements
- Inherits wait strategies from BasePage
- Thread-safe with thread-local WebDriver instances
- Behavioral equivalence with Java PageFactory implementation

**Technical Debt Summary:**
- 2 duplicate locator pairs requiring application-side fixes
- 1 brittle index-based locator needing date-based alternative
- 2 potentially dynamic ID attributes requiring verification

**Migration Status:** ✅ Complete - Functionally equivalent to CalendarP.java

