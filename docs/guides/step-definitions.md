# Writing Step Definitions

## Overview

Step definitions are the bridge between your Gherkin feature files and your Python automation code. They connect the human-readable test scenarios to the actual WebDriver interactions and page object methods that perform the test actions.

In Behave, step definitions are Python functions decorated with `@given`, `@when`, `@then`, or `@step` decorators that match specific text patterns from your feature files. When Behave runs a scenario, it matches each step in the feature file to its corresponding step definition function and executes it.

### What You'll Learn

This guide covers:

- **Step decorator usage** - How to use @given/@when/@then decorators
- **Context object** - Sharing state between steps with context.driver and context.config
- **Parameterized steps** - Using angle brackets and quotes for dynamic values
- **Page object integration** - Calling page object methods from steps
- **Configuration access** - Retrieving test data from config.yaml and .env
- **Best practices** - Writing maintainable, reusable step definitions
- **Troubleshooting** - Solving common step definition issues

### Prerequisites

Before writing step definitions, you should:

- Understand Gherkin syntax and feature files (see [Feature Files Guide](feature-files.md))
- Understand the Page Object Model pattern (see [Page Object Model Guide](page-object-model.md))
- Have the framework installed and configured
- Be familiar with Python functions and decorators

## Step Decorators

Behave provides four decorators to match steps in your feature files:

### @given - Preconditions and Setup

Use `@given` for steps that set up the initial state of your test. These steps establish preconditions before any actions are performed.

**Example:**

```python
from behave import given
from utilities.config_reader import ConfigReader

@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """Navigate to login page using configured URL from config.yaml."""
    config_reader = ConfigReader()
    login_url = config_reader.get_property('web.table.url')
    context.driver.get(login_url)
```

**Source:** `features/steps/login_steps.py:90-136`

**Gherkin Usage:**

```gherkin
Scenario: User logs in with valid credentials
  Given User is on the upgenix login page
  When User enters "salesmanager7@info.com" username
  Then User should see the dashboard
```

### @when - Actions and Interactions

Use `@when` for steps that perform actions or trigger events. These steps represent user interactions with the application.

**Example:**

```python
from behave import when
from pages.login_page import LoginPage

@when('User clicks the login button')
def step_click_login_button(context):
    """Click the login button to submit authentication credentials."""
    login_page = LoginPage(context.driver)
    login_page.login_button.click()
```

**Source:** `features/steps/login_steps.py:240-286`

**Gherkin Usage:**

```gherkin
When User clicks the login button
```

### @then - Assertions and Verifications

Use `@then` for steps that verify outcomes and assert expected results. These steps validate that the application behaves correctly.

**Example:**

```python
from behave import then
from pages.login_page import LoginPage

@then('User should see the dashboard')
def step_verify_dashboard(context):
    """Verify successful login by validating dashboard appears and page title is 'Odoo'."""
    login_page = LoginPage(context.driver)
    
    # Wait for dashboard element to be visible
    dashboard_element = login_page.dashboard
    assert dashboard_element.is_displayed(), \
        "Dashboard element not displayed after login"
    
    # Verify page title
    expected_title = "Odoo"
    actual_title = context.driver.title
    assert actual_title == expected_title, \
        f"Page title mismatch! Expected: '{expected_title}', Actual: '{actual_title}'"
```

**Source:** `features/steps/login_steps.py:341-418`

**Gherkin Usage:**

```gherkin
Then User should see the dashboard
```

### @step - Universal Matcher

Use `@step` for steps that work with any keyword (Given/When/Then/And/But). This is useful for reusable steps that can appear in different contexts.

**Example:**

```python
from behave import step
from pages.calendar_page import CalendarPage

@step("User click on desired date time")
def user_click_on_desired_date_time(context):
    """Click on a specific date cell to open the meeting creation dialog."""
    calendar_page = CalendarPage(context.driver)
    calendar_page.date_box.click()
```

**Source:** `features/steps/calendar_steps.py:372-408`

**Gherkin Usage:**

```gherkin
And User click on desired date time
# or
When User click on desired date time
# or
Given User click on desired date time
```

## Context Object

The `context` object is Behave's mechanism for sharing state between steps within a scenario. It's passed as the first parameter to every step definition function.

### Context Attributes

#### context.driver - WebDriver Instance

Access the thread-local WebDriver instance for browser interactions:

```python
@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    # Access WebDriver through context
    context.driver.get("https://example.com")
    
    # Get page title
    title = context.driver.title
    
    # Find element directly (though page objects are preferred)
    element = context.driver.find_element(By.ID, "login")
```

**Thread Safety Note:** The `context.driver` uses `threading.local()` from `DriverManager`, ensuring each parallel test execution has its own isolated WebDriver instance. This prevents test interference when running tests in parallel with `pytest-xdist` or `behave-parallel`.

**Source:** `features/steps/login_steps.py:122-136`

#### context.config - Configuration Access

While not directly stored on context, you can access configuration through ConfigReader:

```python
from utilities.config_reader import ConfigReader

@given('User is on the login page')
def step_navigate_to_login(context):
    config_reader = ConfigReader()
    
    # Get configuration values
    base_url = config_reader.get_property('web.table.url')
    timeout = config_reader.get_property('timeout.explicit')
    
    context.driver.get(base_url)
```

**Source:** `features/steps/login_steps.py:126-128`

### Storing Custom Data in Context

You can store custom data in context to share between steps:

```python
@when('User creates a meeting named "{meeting_name}"')
def step_create_meeting(context, meeting_name):
    calendar_page = CalendarPage(context.driver)
    calendar_page.create_meeting(meeting_name)
    
    # Store meeting name for later verification
    context.created_meeting_name = meeting_name

@then('User should see the created meeting')
def step_verify_meeting(context):
    calendar_page = CalendarPage(context.driver)
    
    # Retrieve stored meeting name
    expected_name = context.created_meeting_name
    actual_name = calendar_page.get_meeting_name()
    
    assert actual_name == expected_name
```

**Best Practice:** Store only data that needs to be shared between steps. Don't use context as a dumping ground for all test data.

## Parameterized Steps

Parameterized steps allow you to write reusable step definitions that accept dynamic values from your feature files.

### Using Quotes for String Parameters

Capture string parameters using quotes in the step text:

```python
@when('User enters "{username}" username')
def step_enter_username(context, username):
    """Enter username into login form email input field."""
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)
```

**Source:** `features/steps/login_steps.py:142-186`

**Gherkin Usage:**

```gherkin
When User enters "salesmanager7@info.com" username
And User enters "posmanager5@info.com" username
```

The text within quotes (`"salesmanager7@info.com"`) is captured and passed as the `username` parameter to the function.

### Using Angle Brackets for Scenario Outline Parameters

When using Scenario Outlines with Examples tables, use angle brackets in your Gherkin:

**Feature File:**

```gherkin
Scenario Outline: Users log in with valid credentials
  Given User is on the upgenix login page
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  Then User should see the dashboard

  Examples:
    | username                  | password     |
    | salesmanager7@info.com    | salesmanager |
    | posmanager5@info.com      | posmanager   |
```

**Step Definition:**

```python
@when('User enters "{username}" username')
def step_enter_username(context, username):
    """Enter username - supports parameterized input from Scenario Outline."""
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)
```

**How It Works:**

1. Behave replaces `<username>` with values from Examples table
2. First iteration: `When User enters "salesmanager7@info.com" username`
3. Second iteration: `When User enters "posmanager5@info.com" username`
4. Step definition receives the actual value as `username` parameter

**Source:** `features/steps/login_steps.py:142-186`

### Multiple Parameters

Capture multiple parameters in a single step:

```python
@then('User sees "{alert_message}" message')
def step_verify_validation_message(context, alert_message):
    """Verify field validation message matches expected text."""
    email_input = context.driver.find_element(By.NAME, "login")
    actual_message = email_input.get_attribute("validationMessage")
    
    assert actual_message == alert_message, \
        f"Validation message mismatch! Expected: '{alert_message}', Actual: '{actual_message}'"
```

**Source:** `features/steps/login_steps.py:484-559`

**Gherkin Usage:**

```gherkin
Then User sees "Please fill out this field." message
Then User sees "Veuillez renseigner ce champ." message
```

## Step Implementation Patterns

### Basic Pattern: Decorator → Function → Page Object → Action

The standard pattern for step definitions:

```python
from behave import when                    # 1. Import decorator
from pages.calendar_page import CalendarPage  # 2. Import page object

@when("User click on the calendar dashboard")   # 3. Decorate with step text
def user_clicks_on_the_calendar_dashboard(context):  # 4. Function with context
    """Navigate to the calendar module."""           # 5. Docstring
    
    # 6. Instantiate page object with context.driver
    calendar_page = CalendarPage(context.driver)
    
    # 7. Call page object method
    calendar_page.calendar_button.click()
```

**Source:** `features/steps/calendar_steps.py:57-89`

### Pattern with Configuration

Access configuration values in steps:

```python
from behave import given
from pages.login_page import LoginPage
from utilities.config_reader import ConfigReader

@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """Navigate to login page using configured URL."""
    
    # Access configuration
    config_reader = ConfigReader()
    login_url = config_reader.get_property('web.table.url')
    
    # Navigate using WebDriver
    context.driver.get(login_url)
```

**Source:** `features/steps/login_steps.py:90-136`

### Pattern with Wait Strategy

Use page object properties that include wait logic:

```python
from behave import then
from pages.login_page import LoginPage

@then('User should see the dashboard')
def step_verify_dashboard(context):
    """Verify dashboard appears after login."""
    login_page = LoginPage(context.driver)
    
    # Property automatically waits for visibility
    dashboard_element = login_page.dashboard
    
    # Verify element is displayed
    assert dashboard_element.is_displayed()
```

**Source:** `features/steps/login_steps.py:341-418`

**Note:** The `login_page.dashboard` property uses `BasePage.wait_for_visibility()` internally, eliminating the need for explicit waits in step definitions.

### Pattern with Assertion

Always include descriptive error messages in assertions:

```python
from behave import then
from pages.login_page import LoginPage

@then('User sees error message')
def step_verify_error_message(context):
    """Verify error message alert is displayed for invalid credentials."""
    login_page = LoginPage(context.driver)
    
    # Get error alert element
    error_alert = login_page.alert_error_message
    
    # Assert with descriptive message
    assert error_alert.is_displayed(), \
        "Error message alert not displayed after invalid login attempt"
```

**Source:** `features/steps/login_steps.py:420-482`

### Pattern with Logging

Include logging for test diagnostics and debugging:

```python
import logging
from behave import when
from pages.calendar_page import CalendarPage

logger = logging.getLogger(__name__)

@when("User click on week button")
def user_clicks_on_week_button(context):
    """Switch calendar view to week mode."""
    logger.info("Step: User clicks on week button")
    
    calendar_page = CalendarPage(context.driver)
    
    logger.debug("Clicking week button to switch to week view")
    calendar_page.week.click()
    
    logger.info("Successfully switched to week view")
```

**Source:** `features/steps/calendar_steps.py:124-153`

**Logging Levels:**
- `logger.info()` - Important step execution milestones
- `logger.debug()` - Detailed execution information
- `logger.error()` - Error conditions
- `logger.warning()` - Warning conditions

## Step Reusability Strategies

### Generic Step Definitions

Write steps that work across multiple features:

```python
@when('User clicks the "{button_name}" button')
def step_click_button(context, button_name):
    """Generic button click step - works for any button."""
    # This step works for login button, save button, create button, etc.
    page = BasePage(context.driver)
    button = page.find_element_by_text(button_name)
    button.click()
```

### Step Composition

Reuse existing steps within other steps:

```python
@when('User logs in with valid credentials')
def step_login_with_valid_credentials(context):
    """Composite step that reuses other steps."""
    # Reuse existing step definitions
    context.execute_steps('''
        Given User is on the upgenix login page
        When User enters "salesmanager7@info.com" username
        And User enters "salesmanager" password
        And User clicks the login button
    ''')
```

**Warning:** Use step composition sparingly. It can make debugging difficult and hide test intent.

### Shared Step Libraries

Organize commonly used steps in a shared module:

**File: `features/steps/common_steps.py`**

```python
from behave import given, when, then

@given('User waits {seconds:d} seconds')
def step_wait_seconds(context, seconds):
    """Wait for specified number of seconds."""
    import time
    time.sleep(seconds)

@then('Page title should be "{expected_title}"')
def step_verify_page_title(context, expected_title):
    """Verify browser page title."""
    actual_title = context.driver.title
    assert actual_title == expected_title
```

Behave automatically discovers all step definitions in the `features/steps/` directory.

## Accessing Configuration in Steps

### Getting Configuration Properties

Use `ConfigReader` to access values from `config.yaml`:

```python
from utilities.config_reader import ConfigReader

@given('User navigates to login page')
def step_navigate_to_login(context):
    config_reader = ConfigReader()
    
    # Get base URL from config.yaml
    base_url = config_reader.get_property('web.table.url')
    
    # Get timeout configuration
    timeout = config_reader.get_property('timeout.explicit')
    
    context.driver.get(base_url)
```

**Configuration File (`config.yaml`):**

```yaml
web:
  table:
    url: "https://testinium.example.com"

timeout:
  explicit: 10
  page_load: 30
```

### Getting Configuration with Defaults

Provide fallback values for optional configuration:

```python
config_reader = ConfigReader()

# Get with default value if key not found
screenshot_dir = config_reader.get_property_or_default(
    'screenshots.directory', 
    'screenshots'
)
```

### Accessing Environment Variables

Environment variables override config.yaml values:

```python
import os

@given('User navigates to application')
def step_navigate_to_app(context):
    # Environment variable takes precedence
    base_url = os.getenv('BASE_URL') or \
               ConfigReader().get_property('web.table.url')
    
    context.driver.get(base_url)
```

**Environment Variable (`.env`):**

```bash
BASE_URL=https://staging.testinium.example.com
```

## Complete Code Examples

### Example 1: Login Flow with Multiple Steps

**Feature File:**

```gherkin
Scenario: User logs in with valid credentials
  Given User is on the upgenix login page
  When User enters "salesmanager7@info.com" username
  And User enters "salesmanager" password
  And User clicks the login button
  Then User should see the dashboard
```

**Step Definitions:**

```python
import logging
from behave import given, when, then
from pages.login_page import LoginPage
from utilities.config_reader import ConfigReader

logger = logging.getLogger(__name__)

@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """Navigate to login page using configured URL."""
    logger.info("Navigating to login page")
    
    config_reader = ConfigReader()
    login_url = config_reader.get_property('web.table.url')
    
    context.driver.get(login_url)
    logger.info(f"Successfully navigated to {login_url}")

@when('User enters "{username}" username')
def step_enter_username(context, username):
    """Enter username into login form."""
    logger.info(f"Entering username: {username}")
    
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)

@when('User enters "{password}" password')
def step_enter_password(context, password):
    """Enter password into login form."""
    logger.info("Entering password (value not logged for security)")
    
    login_page = LoginPage(context.driver)
    login_page.input_password.send_keys(password)

@when('User clicks the login button')
def step_click_login_button(context):
    """Click login button to submit credentials."""
    logger.info("Clicking login button")
    
    login_page = LoginPage(context.driver)
    login_page.login_button.click()

@then('User should see the dashboard')
def step_verify_dashboard(context):
    """Verify dashboard appears with correct title."""
    logger.info("Verifying dashboard visibility")
    
    login_page = LoginPage(context.driver)
    
    # Wait for dashboard element
    dashboard_element = login_page.dashboard
    assert dashboard_element.is_displayed(), \
        "Dashboard not displayed after login"
    
    # Verify page title
    expected_title = "Odoo"
    actual_title = context.driver.title
    assert actual_title == expected_title, \
        f"Title mismatch! Expected: '{expected_title}', Actual: '{actual_title}'"
    
    logger.info("Dashboard verification successful")
```

**Source:** `features/steps/login_steps.py:90-418`

### Example 2: Calendar Meeting Creation with Parameterization

**Feature File:**

```gherkin
Scenario Outline: User creates meetings with different names
  Given User is on the calendar page
  When User click on desired date time
  Then User enters "<meeting_name>" in the box and clicks the create button
  When User can see all the note
  
  Examples:
    | meeting_name         |
    | Team Standup         |
    | Client Review        |
    | Sprint Planning      |
```

**Step Definitions:**

```python
import logging
from behave import given, when, then, step
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.calendar_page import CalendarPage

logger = logging.getLogger(__name__)

@step("User click on desired date time")
def user_click_on_desired_date_time(context):
    """Click on a date cell to open meeting creation dialog."""
    logger.info("Step: User clicks on desired date time")
    
    calendar_page = CalendarPage(context.driver)
    
    # Click date box to open dialog
    calendar_page.date_box.click()
    
    # Wait for create note modal
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.create_note))
    
    # Verify modal is displayed
    assert calendar_page.create_note.is_displayed(), \
        "Create note modal not displayed after clicking date box"
    
    logger.info("Meeting creation dialog opened successfully")

@then('User enters "{note}" in the box and clicks the create button')
def user_enters_note_in_the_box_and_clicks_the_create_button(context, note):
    """Enter meeting summary and create the meeting."""
    logger.info(f"Creating meeting: '{note}'")
    
    calendar_page = CalendarPage(context.driver)
    
    # Enter note text
    calendar_page.summary_box.send_keys(note)
    
    # Click create button
    calendar_page.create_button.click()
    
    # Wait for note to be created
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.get_note))
    
    # Validate created note text
    created_note_text = calendar_page.get_note.text
    assert created_note_text == note, \
        f"Note text mismatch! Expected: '{note}', Got: '{created_note_text}'"
    
    logger.info(f"Meeting '{note}' created successfully")

@when("User can see all the note")
def user_can_see_all_the_note(context):
    """Verify the created note is visible."""
    logger.info("Verifying note visibility")
    
    calendar_page = CalendarPage(context.driver)
    
    # Wait for created note
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of(calendar_page.created_note))
    
    # Verify note is displayed
    assert calendar_page.created_note.is_displayed(), \
        "Created note not visible in calendar"
    
    logger.info("Note visibility verified")
```

**Source:** `features/steps/calendar_steps.py:372-498`

## Best Practices for Step Definitions

### 1. One Action Per Step

Each step definition should perform a single, focused action:

**Good:**

```python
@when('User enters "{username}" username')
def step_enter_username(context, username):
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)
```

**Bad:**

```python
@when('User logs in with "{username}" and "{password}"')
def step_login(context, username, password):
    # Too much in one step - breaks single responsibility
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)
    login_page.input_password.send_keys(password)
    login_page.login_button.click()
```

### 2. Use Declarative Intent

Step definitions should describe *what* is being tested, not *how*:

**Good:**

```gherkin
When User enters valid credentials
And User clicks the login button
Then User should see the dashboard
```

**Bad:**

```gherkin
When User finds element by ID "email" and sends keys "user@example.com"
And User finds element by CSS selector ".submit-btn" and clicks it
Then User finds element by XPath "//div[@class='dashboard']" and verifies visibility
```

### 3. Avoid Technical Details in Steps

Keep step definitions at a business/user level:

**Good:**

```python
@when('User creates a new meeting')
def step_create_meeting(context):
    calendar_page = CalendarPage(context.driver)
    calendar_page.create_meeting("Team Standup")
```

**Bad:**

```python
@when('User clicks XPath "//button[@id=\'create\']"')
def step_click_xpath(context):
    element = context.driver.find_element(By.XPATH, "//button[@id='create']")
    element.click()
```

### 4. Use Proper Wait Strategies

Always use explicit waits through page object properties:

**Good:**

```python
@then('Dashboard is visible')
def step_verify_dashboard(context):
    login_page = LoginPage(context.driver)
    # Property includes wait_for_visibility
    dashboard = login_page.dashboard
    assert dashboard.is_displayed()
```

**Bad:**

```python
@then('Dashboard is visible')
def step_verify_dashboard(context):
    import time
    time.sleep(3)  # Never use time.sleep()!
    dashboard = context.driver.find_element(By.ID, "dashboard")
    assert dashboard.is_displayed()
```

**See also:** [Wait Strategies Guide](wait-strategies.md)

### 5. Include Meaningful Assertions

Always provide descriptive error messages:

**Good:**

```python
assert actual_title == expected_title, \
    f"Page title mismatch! Expected: '{expected_title}', Actual: '{actual_title}'"
```

**Bad:**

```python
assert actual_title == expected_title  # No error message!
```

### 6. Write Comprehensive Docstrings

Every step definition must have a docstring:

```python
@when('User enters "{username}" username')
def step_enter_username(context, username):
    """
    Enter username into login form email input field.
    
    This step supports parameterized username input from Scenario Outline Examples
    tables, enabling data-driven testing with multiple user credentials.
    
    Args:
        context: Behave context object containing WebDriver instance
        username: Parameterized username value from Examples table
    
    Raises:
        TimeoutException: If email input element not found within default timeout
        WebDriverException: If send_keys operation fails
    
    Example:
        When User enters "salesmanager7@info.com" username
    """
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)
```

**Source:** `features/steps/login_steps.py:142-186`

### 7. Handle Sensitive Data Appropriately

Never log passwords or sensitive information:

```python
@when('User enters "{password}" password')
def step_enter_password(context, password):
    """Enter password into login form."""
    logger.info("Entering password (value not logged for security)")
    # NOT: logger.info(f"Entering password: {password}")
    
    login_page = LoginPage(context.driver)
    login_page.input_password.send_keys(password)
```

**Source:** `features/steps/login_steps.py:188-238`

## Step Organization Strategies

### Organize by Feature

Group related step definitions in feature-specific modules:

```
features/steps/
├── __init__.py
├── login_steps.py          # All login-related steps
├── calendar_steps.py       # All calendar-related steps
├── crm_steps.py           # All CRM-related steps
├── employee_steps.py      # All employee-related steps
└── common_steps.py        # Shared steps used across features
```

### Shared Steps Module

Create a `common_steps.py` for steps used across multiple features:

```python
# features/steps/common_steps.py
from behave import given, when, then

@given('User waits for page to load')
def step_wait_for_page_load(context):
    """Wait for page load to complete."""
    # Shared wait logic
    pass

@then('Page title should be "{expected_title}"')
def step_verify_page_title(context, expected_title):
    """Verify browser page title."""
    actual_title = context.driver.title
    assert actual_title == expected_title
```

### Avoid Duplication

If multiple features need the same step, define it once in `common_steps.py`:

**Don't do this:**

```python
# features/steps/login_steps.py
@then('Page title should be "{expected_title}"')
def step_verify_title_login(context, expected_title):
    assert context.driver.title == expected_title

# features/steps/calendar_steps.py
@then('Page title should be "{expected_title}"')
def step_verify_title_calendar(context, expected_title):
    assert context.driver.title == expected_title
```

**Do this:**

```python
# features/steps/common_steps.py
@then('Page title should be "{expected_title}"')
def step_verify_page_title(context, expected_title):
    """Verify page title - used across all features."""
    assert context.driver.title == expected_title
```

## Troubleshooting

### Issue: Step Not Found

**Symptom:**

```
No step implementation found for step
  When User enters "test@example.com" username
```

**Causes:**

1. **Step text doesn't match exactly** - Behave is case-sensitive and whitespace-sensitive
2. **Step definition not in `features/steps/` directory**
3. **Step definition module not imported**

**Solutions:**

1. **Check exact text match:**

   ```python
   # Feature file
   When User enters "test" username
   
   # Step definition - must match EXACTLY
   @when('User enters "{username}" username')  # ✓ Correct
   @when('User enters {username} username')    # ✗ Missing quotes
   @when('user enters "{username}" username')  # ✗ Wrong case
   ```

2. **Verify file location:**

   ```
   features/
   └── steps/
       ├── __init__.py          # Must exist!
       └── login_steps.py       # Your step definitions
   ```

3. **Check Behave discovery:**

   ```bash
   # List all discovered steps
   behave --dry-run --no-summary
   ```

### Issue: Context Attribute Error

**Symptom:**

```
AttributeError: 'Context' object has no attribute 'driver'
```

**Cause:** WebDriver not initialized in `environment.py` hooks.

**Solution:** Verify `features/environment.py` contains:

```python
from utilities.driver_manager import DriverManager

def before_scenario(context, scenario):
    """Initialize WebDriver before each scenario."""
    context.driver = DriverManager.get_driver()

def after_scenario(context, scenario):
    """Quit WebDriver after each scenario."""
    DriverManager.quit_driver()
```

### Issue: Page Object Element Not Found

**Symptom:**

```
TimeoutException: Message: Element not found within timeout
```

**Causes:**

1. **Element not yet visible** - Page still loading
2. **Wrong locator** - Element locator incorrect
3. **Element in iframe** - Need to switch iframe context

**Solutions:**

1. **Use page object properties with built-in waits:**

   ```python
   # Good - property includes wait_for_visibility
   login_page = LoginPage(context.driver)
   element = login_page.input_email
   ```

2. **Verify locator in browser DevTools:**

   ```python
   # In browser console, test locator
   document.querySelector('input[name="login"]')
   ```

3. **Check for iframes:**

   ```python
   # Switch to iframe if element is inside
   context.driver.switch_to.frame("iframe_name")
   element = login_page.input_email
   context.driver.switch_to.default_content()
   ```

### Issue: Stale Element Reference

**Symptom:**

```
StaleElementReferenceException: stale element reference: 
element is not attached to the page document
```

**Cause:** Element retrieved once, then page changed (AJAX, navigation, etc.)

**Solution:** Use page object properties instead of storing elements:

**Bad:**

```python
@when('User performs multiple actions')
def step_multiple_actions(context):
    login_page = LoginPage(context.driver)
    
    # Store element reference
    email_input = login_page.input_email
    
    # Some action that updates DOM
    some_action_that_refreshes_page()
    
    # Element is now stale!
    email_input.send_keys("test")  # ✗ StaleElementReferenceException
```

**Good:**

```python
@when('User performs multiple actions')
def step_multiple_actions(context):
    login_page = LoginPage(context.driver)
    
    # Get fresh element each time
    login_page.input_email.send_keys("test1")
    
    some_action_that_refreshes_page()
    
    # Get fresh element again - property re-finds element
    login_page.input_email.send_keys("test2")  # ✓ Works!
```

### Issue: Timing Problems in Parallel Execution

**Symptom:** Tests pass individually but fail when run in parallel.

**Cause:** Shared state or improper thread-local driver usage.

**Solution:** Verify `DriverManager` uses `threading.local()`:

```python
# utilities/driver_manager.py
import threading

class DriverManager:
    _driver_storage = threading.local()
    
    @classmethod
    def get_driver(cls):
        """Get thread-local WebDriver instance."""
        if not hasattr(cls._driver_storage, 'driver'):
            cls._driver_storage.driver = cls._create_driver()
        return cls._driver_storage.driver
```

**See also:** [Parallel Execution Guide](parallel-execution.md)

## See Also

- **[Feature Files Guide](feature-files.md)** - Writing Gherkin scenarios
- **[Page Object Model Guide](page-object-model.md)** - Creating page objects for step definitions
- **[Wait Strategies Guide](wait-strategies.md)** - Explicit waits and timing strategies
- **[Configuration Management Guide](configuration-management.md)** - Accessing config.yaml and .env
- **[Parallel Execution Guide](parallel-execution.md)** - Thread-safety considerations

## API Reference

- **[Login Steps API](../api-reference/steps/login-steps.md)** - Complete login step definitions reference
- **[Calendar Steps API](../api-reference/steps/calendar-steps.md)** - Calendar step definitions reference
- **[BasePage API](../api-reference/pages/base-page.md)** - Page object base class used in steps
- **[Behave Environment Hooks](../api-reference/features/environment.md)** - Setup and teardown hooks

---

**Source Examples:**
- Login step definitions: `features/steps/login_steps.py`
- Calendar step definitions: `features/steps/calendar_steps.py`

**Framework Version:** 1.0.0  
**Last Updated:** 2024

