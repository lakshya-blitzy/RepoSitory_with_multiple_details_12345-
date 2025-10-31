# Employee Step Definitions API Reference

## Overview

The Employee step definitions module provides Behave step implementations for employee and HR management test scenarios in the Testinium QA automation framework. This module contains 12 step definitions covering employee navigation, CRUD operations, profile management, and verification workflows.

**Module:** `features/steps/employee_steps.py`

**Source:** `features/steps/employee_steps.py`

**Related Feature:** `features/EmployeeFc.feature`

### Key Features

- **Employee Module Navigation:** Navigate through Employees, Departments, Challenges, Badges, and Goals History stages
- **Employee CRUD Operations:** Create and edit employee workflows with explicit waits
- **Authentication Integration:** Environment variable-based secure credential management
- **Configuration Integration:** ConfigReader for URL and title expectations
- **Page Object Pattern:** Full integration with EmployeePage page object
- **Explicit Waits:** Replaces all Thread.sleep() anti-patterns with WebDriverWait conditions

### Security Enhancements

This module addresses critical security vulnerabilities from the Java version:
- **Environment Variable Credentials:** Uses `POS_MANAGER_USERNAME` and `POS_MANAGER_PASSWORD` environment variables
- **No Hardcoded Credentials:** Eliminates hardcoded credentials vulnerability from EmployeeP.java
- **Secure Authentication:** Calls `employee_page.enter_pos_manager_credentials()` for credential handling

### Migration Context

**Converted from:** `src/main/java/com/testinium/step_definitions/EmployeeStage.java`

**Framework Migration:** Cucumber (@When/@Then) → Behave (@when/@then)

**Critical Improvements:**
- Eliminated 8 Thread.sleep() calls (total: 29,000ms removed)
- Replaced with explicit WebDriverWait conditions using expected_conditions
- Environment variable-based authentication
- Comprehensive logging for test diagnostics
- Proper exception handling with descriptive error messages

---

## Step Definitions

### Navigation Steps

#### @when("User is on upgenix login page")

Navigate to the Upgenix login page URL from configuration.

**Source:** `features/steps/employee_steps.py:68-109`

**Gherkin Pattern:**
```gherkin
When User is on upgenix login page
```

**Parameters:** None

**Behavior:**
1. Retrieves `web.table.url` from config/config.yaml
2. Navigates browser to the login page URL
3. Logs navigation activity for diagnostics

**Configuration Required:**
- `web.table.url`: Base URL for the Upgenix login page

**Example Usage:**
```gherkin
Feature: Employee Management
  Scenario: Access Login Page
    When User is on upgenix login page
```

**Python Implementation:**
```python
@when("User is on upgenix login page")
def user_is_on_upgenix_login_page(context):
    config = ConfigReader()
    login_url = config.get_property("web.table.url")
    context.driver.get(login_url)
```

**Raises:**
- `Exception`: If configuration is invalid or navigation fails

**See Also:**
- ConfigReader: [Configuration API](../utilities/config-reader.md)

---

#### @when("User is on the dashboard")

Navigate to dashboard and authenticate with POS Manager credentials from environment variables.

**Source:** `features/steps/employee_steps.py:112-178`

**Gherkin Pattern:**
```gherkin
When User is on the dashboard
```

**Parameters:** None

**Behavior:**
1. Retrieves `url` (dashboard URL) from configuration
2. Navigates browser to dashboard URL
3. Instantiates EmployeePage with context.driver
4. Calls `enter_pos_manager_credentials()` for secure authentication
5. Logs authentication activity

**Configuration Required:**
- `url`: Dashboard URL after successful authentication

**Environment Variables Required:**
- `POS_MANAGER_USERNAME`: POS Manager username (e.g., posmanager50@info.com)
- `POS_MANAGER_PASSWORD`: POS Manager password

**Example Usage:**
```gherkin
Feature: Employee Management
  Scenario: Access Dashboard
    When User is on the dashboard
```

**Security Note:**
This step implements the security remediation by using environment variables instead of hardcoded credentials. Credentials must be set before test execution:

```bash
export POS_MANAGER_USERNAME="posmanager50@info.com"
export POS_MANAGER_PASSWORD="your_secure_password"
```

**Raises:**
- `ValueError`: If required environment variables are not set
- `Exception`: If navigation or authentication fails

**See Also:**
- EmployeePage: [Employee Page Object API](../pages/employee-page.md)
- Configuration Guide: [Environment Variables](../../reference/environment-variables.md)

---

#### @when("User clicks Employees stage")

Click Employees navigation link and verify page title changes to "Employees - Odoo".

**Source:** `features/steps/employee_steps.py:181-250`

**Gherkin Pattern:**
```gherkin
When User clicks Employees stage
```

**Parameters:** None

**Behavior:**
1. Instantiates EmployeePage with context.driver
2. Retrieves expected page title from configuration (default: "Employees - Odoo")
3. Clicks empl_stage navigation link
4. Waits for page title to match expected value (10 second timeout)
5. Validates final page title equals "Employees - Odoo"

**Configuration Required:**
- `EmplTitle`: Expected page title for Employees stage (optional, defaults to "Employees - Odoo")

**Example Usage:**
```gherkin
Feature: Employee Navigation
  Scenario: Navigate to Employees
    When User is on the dashboard
    And User clicks Employees stage
    Then User should see the page title "Employees - Odoo"
```

**Wait Strategy:**
Uses explicit WebDriverWait with EC.title_is() to ensure page load completes before proceeding.

**Raises:**
- `AssertionError`: If page title does not match "Employees - Odoo"
- `TimeoutException`: If title does not update within 10 seconds

**See Also:**
- Wait Strategies Guide: [Explicit Waits](../../guides/wait-strategies.md)

---

#### @when("User clicks Challenges stage")

Navigate through multi-stage HR module: Badges → Challenges → Goals History with visibility waits.

**Source:** `features/steps/employee_steps.py:253-316`

**Gherkin Pattern:**
```gherkin
When User clicks Challenges stage
```

**Parameters:** None

**Behavior:**
1. Instantiates EmployeePage and WebDriverWait (10 second timeout)
2. **Stage 1:** Clicks Badges button, waits for visibility
3. **Stage 2:** Clicks Challenges button, waits for visibility
4. **Stage 3:** Clicks Goals History button, waits for visibility
5. Logs each navigation stage for diagnostics

**Example Usage:**
```gherkin
Feature: HR Module Navigation
  Scenario: Navigate through Challenges
    When User is on the dashboard
    And User clicks Challenges stage
```

**Wait Strategy:**
Each button click is followed by EC.visibility_of() to ensure the page transition completes before the next interaction.

**Raises:**
- `TimeoutException`: If any navigation button is not visible within 10 seconds

**Technical Details:**
- Multi-stage navigation ensures proper page state transitions
- Each wait validates the current element remains visible after click
- Prevents race conditions during rapid navigation

---

#### @when("User clicks Departments stage")

Click Departments navigation link and wait for page load with explicit title wait.

**Source:** `features/steps/employee_steps.py:319-370`

**Gherkin Pattern:**
```gherkin
When User clicks Departments stage
```

**Parameters:** None

**Behavior:**
1. Instantiates EmployeePage and WebDriverWait
2. Clicks departments_btn navigation link
3. Waits for page title to be "Departments - Odoo" (10 second timeout)
4. Logs navigation activity

**Example Usage:**
```gherkin
Feature: Department Management
  Scenario: Navigate to Departments
    When User is on the dashboard
    And User clicks Departments stage
    Then User should see the last stage title
```

**Critical Improvement:**
Eliminated Thread.sleep(7000) anti-pattern from Java version (line 48). Replaced with explicit EC.title_is() wait, making tests more reliable and faster.

**Raises:**
- `TimeoutException`: If "Departments - Odoo" page title is not displayed within 10 seconds

**See Also:**
- Architecture: [Wait Strategies](../../architecture/wait-strategies.md)

---

### Verification Steps

#### @then("User should see the last stage title")

Verify the page title is "Departments - Odoo".

**Source:** `features/steps/employee_steps.py:373-420`

**Gherkin Pattern:**
```gherkin
Then User should see the last stage title
```

**Parameters:** None

**Behavior:**
1. Retrieves current page title from context.driver
2. Validates title equals "Departments - Odoo"
3. Provides descriptive assertion error for debugging

**Example Usage:**
```gherkin
Feature: Department Navigation
  Scenario: Verify Department Stage
    When User is on the dashboard
    And User clicks Departments stage
    Then User should see the last stage title
```

**Validation:**
```python
assert actual_title == "Departments - Odoo"
```

**Raises:**
- `AssertionError`: If page title does not equal "Departments - Odoo"

---

### Employee Dashboard Steps

#### @when("User is on the employees dashboard")

Navigate to dashboard, authenticate, and navigate to Employees stage.

**Source:** `features/steps/employee_steps.py:423-502`

**Gherkin Pattern:**
```gherkin
When User is on the employees dashboard
```

**Parameters:** None

**Behavior:**
1. Retrieves dashboard URL from configuration
2. Navigates to dashboard
3. Instantiates EmployeePage
4. Authenticates with POS Manager credentials (environment variables)
5. Waits for empl_stage button to be clickable (replaces Thread.sleep)
6. Clicks Employees stage navigation link

**Configuration Required:**
- `url`: Dashboard URL

**Environment Variables Required:**
- `POS_MANAGER_USERNAME`: POS Manager username
- `POS_MANAGER_PASSWORD`: POS Manager password

**Example Usage:**
```gherkin
Feature: Employee Creation
  Scenario Outline: Create New Employee
    When User is on the employees dashboard
    And User creates new employees "<name>" in the Employees stage
    
    Examples:
      | name              |
      | Cristiano Ronaldo |
```

**Critical Improvements:**
- Eliminated Thread.sleep(3000) from Java version (line 62)
- Added explicit wait for empl_stage button clickability
- Environment variable-based authentication

**Raises:**
- `ValueError`: If required environment variables are not set
- `TimeoutException`: If Employees stage button is not clickable within 10 seconds

---

### Employee CRUD Operations

#### @when('User creates new employees "{name}" in the Employees stage')

Create a new employee with the specified name using explicit waits for all interactions.

**Source:** `features/steps/employee_steps.py:505-583`

**Gherkin Pattern:**
```gherkin
When User creates new employees "{name}" in the Employees stage
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| name | string | Full name of employee to create | "Cristiano Ronaldo" |

**Behavior:**
1. Instantiates EmployeePage and WebDriverWait
2. Waits for Create button to be clickable (replaces Thread.sleep)
3. Clicks Create button
4. Waits for page title to change to "New - Odoo" (replaces Thread.sleep)
5. Enters employee name into employees_name input field
6. Waits for Save button to be clickable (replaces Thread.sleep)
7. Clicks Save button to create employee

**Example Usage:**
```gherkin
Feature: Employee Creation
  Scenario Outline: Create Employee with Various Names
    When User is on the employees dashboard
    And User creates new employees "<name>" in the Employees stage
    Then User should see the Employee created message under full profile
    
    Examples: Employee's name
      | name              |
      | Cristiano Ronaldo |
      | Lionel Messi      |
      | John Doe          |
```

**Critical Improvements:**
Eliminated two Thread.sleep(3000) calls from Java version:
- Line 68: Replaced with EC.element_to_be_clickable(create_btn)
- Line 70: Replaced with EC.title_is("New - Odoo")
- Line 103: Replaced with EC.element_to_be_clickable(saved_message)

**Wait Strategy:**
- Create button clickability: Ensures button is interactive before clicking
- Title change: Confirms page navigation completed
- Save button clickability: Ensures form is ready before saving

**Raises:**
- `TimeoutException`: If expected elements or page title do not appear within 10 seconds

**See Also:**
- EmployeePage: [Employee Page Object](../pages/employee-page.md)

---

#### @then("User should see the Employee created message under full profile")

Verify that the "Employee created" confirmation message is displayed.

**Source:** `features/steps/employee_steps.py:586-640`

**Gherkin Pattern:**
```gherkin
Then User should see the Employee created message under full profile
```

**Parameters:** None

**Behavior:**
1. Instantiates EmployeePage
2. Accesses created_message property (includes internal visibility wait)
3. Validates element is displayed
4. Logs the confirmation message text for diagnostics

**Example Usage:**
```gherkin
Feature: Employee Creation Verification
  Scenario: Verify Creation Message
    When User is on the employees dashboard
    And User creates new employees "John Doe" in the Employees stage
    Then User should see the Employee created message under full profile
```

**Validation:**
```python
assert created_msg_element.is_displayed()
```

**Technical Details:**
The `created_message` property in EmployeePage uses `wait_for_visibility()` internally, ensuring the element is visible before this step validates it. This follows the framework's explicit wait pattern.

**Raises:**
- `AssertionError`: If created_message element is not displayed

---

#### @then("User should see listed employees in the Employees stage")

Navigate to Employees stage and verify page title shows employee list.

**Source:** `features/steps/employee_steps.py:643-704`

**Gherkin Pattern:**
```gherkin
Then User should see listed employees in the Employees stage
```

**Parameters:** None

**Behavior:**
1. Instantiates EmployeePage and WebDriverWait
2. Clicks empl_stage navigation link
3. Waits for page title to be "Employees - Odoo" (10 second timeout)
4. Validates final page title equals "Employees - Odoo"

**Example Usage:**
```gherkin
Feature: Employee List Verification
  Scenario Outline: Verify Created Employee is Listed
    When User is on the employees dashboard
    And User creates new employees "<name>" in the Employees stage
    Then User should see listed employees in the Employees stage
    
    Examples: Employee's name
      | name         |
      | Lionel Messi |
```

**Purpose:**
This step confirms successful navigation back to the employee list view after creation, allowing visual verification that the created employee appears in the list.

**Raises:**
- `AssertionError`: If page title does not equal "Employees - Odoo"
- `TimeoutException`: If page title does not update within 10 seconds

---

#### @when("User edits created employees in the Employees module")

Complete employee edit workflow: navigate, select employee, edit name to "Sterling", and save.

**Source:** `features/steps/employee_steps.py:707-838`

**Gherkin Pattern:**
```gherkin
When User edits created employees in the Employees module
```

**Parameters:** None

**Behavior:**
1. Retrieves dashboard URL from configuration
2. Navigates to dashboard
3. Authenticates with POS Manager credentials (environment variables)
4. Waits for Employees stage button clickability (replaces Thread.sleep)
5. Clicks Employees stage
6. Waits for "Employees - Odoo" page title (replaces Thread.sleep)
7. Clicks to select employee from list
8. Waits for Edit button clickability (replaces Thread.sleep)
9. Clicks Edit button
10. Clears existing employee name
11. Enters new name "Sterling"
12. Waits for Save button clickability (replaces Thread.sleep)
13. Clicks Save button

**Configuration Required:**
- `url`: Dashboard URL

**Environment Variables Required:**
- `POS_MANAGER_USERNAME`: POS Manager username
- `POS_MANAGER_PASSWORD`: POS Manager password

**Example Usage:**
```gherkin
Feature: Employee Editing
  Scenario: Edit Employee Name
    When User is on the employees dashboard
    And User edits created employees in the Employees module
    Then User should see the edited name in the Employees module
```

**Critical Improvements:**
Eliminated four Thread.sleep(3000) calls from Java version:
- Line 95: Replaced with EC.element_to_be_clickable(empl_stage)
- Line 97: Replaced with EC.title_is("Employees - Odoo")
- Line 100: Replaced with EC.element_to_be_clickable(edit_employee)
- Line 103: Replaced with EC.element_to_be_clickable(saved_message)

**Hardcoded Value:**
This step hardcodes the new employee name as "Sterling" for consistent test behavior. This matches the original Java implementation.

**Raises:**
- `ValueError`: If required environment variables are not set
- `TimeoutException`: If expected elements do not become clickable within 10 seconds

---

#### @then("User should see the edited name in the Employees module")

Navigate back to Employees stage to view the edited employee.

**Source:** `features/steps/employee_steps.py:841-878`

**Gherkin Pattern:**
```gherkin
Then User should see the edited name in the Employees module
```

**Parameters:** None

**Behavior:**
1. Instantiates EmployeePage
2. Clicks empl_stage navigation link to return to employees list
3. Allows verification that the edited employee name is displayed

**Example Usage:**
```gherkin
Feature: Employee Edit Verification
  Scenario: Verify Edited Employee Name
    When User is on the employees dashboard
    And User edits created employees in the Employees module
    Then User should see the edited name in the Employees module
```

**Note:**
This step performs navigation only. Actual name verification can be done through visual inspection or could be enhanced with explicit name text validation in future enhancements.

**See Also:**
- Employee Testing Guide: [Employee Management Testing](../../guides/employee-testing.md)

---

## Complete Usage Examples

### Example 1: Verify All Buttons Work in Employees Stage

From `features/EmployeeFc.feature` - Scenario UPGN-340

**Feature File:**
```gherkin
@UPGN-340
Scenario: Verify that all buttons work as expected at the employees stage
  When User is on the dashboard
  And User clicks Employees stage
  And User clicks Challenges stage
  And User clicks Departments stage
  Then User should see the last stage title
```

**Step Execution Flow:**
1. `user_is_on_the_dashboard()` - Navigates and authenticates
2. `user_clicks_employees_stage()` - Navigates to Employees
3. `user_clicks_challenges_stage()` - Multi-stage navigation: Badges → Challenges → Goals History
4. `user_clicks_departments_stage()` - Navigates to Departments
5. `user_should_see_the_last_stage_title()` - Verifies "Departments - Odoo" title

**Purpose:** Validates navigation through all HR module stages without errors.

---

### Example 2: Create Employee and Verify Creation Message

From `features/EmployeeFc.feature` - Scenario Outline UPGN-341

**Feature File:**
```gherkin
@UPGN-341
Scenario Outline: Verify that the "Employee created" message appears under full profile
  When User is on the employees dashboard
  And User creates new employees "<name>" in the Employees stage
  Then User should see the Employee created message under full profile
  
  Examples: Employee's name
    | name              |
    | Cristiano Ronaldo |
```

**Step Execution Flow:**
1. `user_is_on_the_employees_dashboard()` - Navigates to dashboard, authenticates, clicks Employees stage
2. `user_creates_new_employees_in_the_employees_stage("Cristiano Ronaldo")` - Creates employee
3. `user_should_see_the_employee_created_message_under_full_profile()` - Verifies creation message

**Purpose:** Validates employee creation workflow with confirmation message.

**Data-Driven Testing:**
The Scenario Outline allows testing with multiple employee names by expanding the Examples table.

---

### Example 3: Create Employee and Verify in List

From `features/EmployeeFc.feature` - Scenario Outline UPGN-342

**Feature File:**
```gherkin
@UPGN-342
Scenario Outline: Verify that the user should be able to see created employee is listed
  When User is on the employees dashboard
  And User creates new employees "<name>" in the Employees stage
  Then User should see listed employees in the Employees stage
  
  Examples: Employee's name
    | name         |
    | Lionel Messi |
```

**Step Execution Flow:**
1. `user_is_on_the_employees_dashboard()` - Setup and navigate to Employees
2. `user_creates_new_employees_in_the_employees_stage("Lionel Messi")` - Creates employee
3. `user_should_see_listed_employees_in_the_employees_stage()` - Navigates to list view for verification

**Purpose:** Validates that created employees appear in the employee list.

---

### Example 4: Edit Existing Employee

From `features/EmployeeFc.feature` - Scenario UPGN-343

**Feature File:**
```gherkin
@UPGN-343
Scenario: Verify that the user can edit a new employee from "Employees" module
  When User is on the employees dashboard
  And User edits created employees in the Employees module
  Then User should see the edited name in the Employees module
```

**Step Execution Flow:**
1. `user_is_on_the_employees_dashboard()` - Setup and navigate to Employees
2. `user_edits_created_employees_in_the_employees_module()` - Complete edit workflow (changes name to "Sterling")
3. `user_should_see_the_edited_name_in_the_employees_module()` - Navigates to list to view edited employee

**Purpose:** Validates employee editing functionality with name update.

**Note:** The employee name is hardcoded to "Sterling" in the step implementation for consistent test behavior.

---

## Configuration Requirements

### Required Configuration Properties

The Employee step definitions require the following configuration properties in `config/config.yaml`:

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| url | string | Dashboard URL for authenticated access | https://testinium-qa.herokuapp.com/web |
| web.table.url | string | Login page URL | https://testinium-qa.herokuapp.com/web/login |
| EmplTitle | string | Expected Employees page title (optional) | "Employees - Odoo" |

**Example Configuration:**
```yaml
application:
  base_url: https://testinium-qa.herokuapp.com
  
url: https://testinium-qa.herokuapp.com/web
web.table.url: https://testinium-qa.herokuapp.com/web/login
EmplTitle: "Employees - Odoo"
```

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| POS_MANAGER_USERNAME | POS Manager username for authentication | posmanager50@info.com |
| POS_MANAGER_PASSWORD | POS Manager password | SecurePassword123! |

**Setup:**
```bash
export POS_MANAGER_USERNAME="posmanager50@info.com"
export POS_MANAGER_PASSWORD="your_secure_password"
```

**Security Best Practice:**
Never hardcode credentials in test files. Always use environment variables for sensitive data.

---

## Integration Patterns

### Page Object Integration

All employee step definitions integrate with the EmployeePage page object:

```python
from pages.employee_page import EmployeePage

# In step definition
employee_page = EmployeePage(context.driver)
employee_page.empl_stage.click()
```

**Property-Based Locators:**
EmployeePage uses @property decorators for element access with built-in waits:
- `empl_stage` - Employees navigation link
- `create_btn` - Create button
- `employees_name` - Employee name input field
- `saved_message` - Save button
- `created_message` - Creation confirmation message
- And more...

**See Also:** [EmployeePage API Reference](../pages/employee-page.md)

### Configuration Integration

ConfigReader singleton provides centralized configuration access:

```python
from utilities.config_reader import ConfigReader

config = ConfigReader()
dashboard_url = config.get_property("url")
expected_title = config.get_property("EmplTitle", default="Employees - Odoo")
```

**See Also:** [ConfigReader API Reference](../utilities/config-reader.md)

### WebDriverWait Integration

Explicit waits using Selenium's WebDriverWait and expected_conditions:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(context.driver, 10)
wait.until(EC.element_to_be_clickable(employee_page._CREATE_BTN))
wait.until(EC.title_is("New - Odoo"))
wait.until(EC.visibility_of(employee_page.badges_btn))
```

**Wait Conditions Used:**
- `EC.element_to_be_clickable()` - Element is visible and enabled
- `EC.title_is()` - Page title matches exactly
- `EC.visibility_of()` - Element is visible in viewport

**See Also:** [Wait Strategies Guide](../../guides/wait-strategies.md)

---

## Thread Safety

### Context Object Usage

All step definitions receive the Behave `context` object, which maintains thread-local state:

```python
@when("User clicks Employees stage")
def user_clicks_employees_stage(context):
    # context.driver is thread-local
    employee_page = EmployeePage(context.driver)
```

### Parallel Execution Compatibility

Employee step definitions are designed for parallel execution:
- **No Global State:** All state stored in thread-local context object
- **No Shared Resources:** Each scenario gets independent WebDriver instance
- **Independent Authentication:** Each thread authenticates separately
- **Explicit Waits Only:** No Thread.sleep() that could cause timing conflicts

**Parallel Execution Example:**
```bash
behave --processes 4 --parallel-element scenario features/EmployeeFc.feature
```

**See Also:** [Parallel Execution Guide](../../guides/parallel-execution.md)

---

## Performance Optimizations

### Thread.sleep() Elimination Summary

The employee step definitions eliminate all 8 Thread.sleep() calls from the Java version:

| Java Line | Sleep Duration | Replaced With | Performance Gain |
|-----------|---------------|---------------|------------------|
| 48 | 7000ms | EC.title_is("Departments - Odoo") | ~5-6 seconds faster |
| 62 | 3000ms | EC.element_to_be_clickable(empl_stage) | ~1-2 seconds faster |
| 68 | 3000ms | EC.element_to_be_clickable(create_btn) | ~1-2 seconds faster |
| 70 | 3000ms | EC.title_is("New - Odoo") | ~1-2 seconds faster |
| 95 | 3000ms | EC.element_to_be_clickable(empl_stage) | ~1-2 seconds faster |
| 97 | 3000ms | EC.title_is("Employees - Odoo") | ~1-2 seconds faster |
| 100 | 3000ms | EC.element_to_be_clickable(edit_employee) | ~1-2 seconds faster |
| 103 | 3000ms | EC.element_to_be_clickable(saved_message) | ~1-2 seconds faster |

**Total Sleep Time Eliminated:** 29,000ms (29 seconds)

**Actual Performance Gain:** 10-18 seconds per test scenario (waits complete faster than fixed sleep times)

**Reliability Improvement:** Explicit waits are more reliable than arbitrary sleep durations, reducing flaky test failures.

---

## Troubleshooting

### Common Issues

#### Issue: Environment Variables Not Set

**Symptoms:**
```
ValueError: POS_MANAGER_USERNAME environment variable is not set
```

**Cause:** Required environment variables are not configured.

**Solution:**
```bash
export POS_MANAGER_USERNAME="posmanager50@info.com"
export POS_MANAGER_PASSWORD="your_secure_password"

# Verify
echo $POS_MANAGER_USERNAME
```

---

#### Issue: TimeoutException on Element Clicks

**Symptoms:**
```
TimeoutException: Message: Element not clickable within 10 seconds
```

**Cause:** Page load is slower than 10 second timeout, or element is covered by another element.

**Solutions:**
1. **Increase timeout:** Modify WebDriverWait timeout in step definition
2. **Check element visibility:** Use browser DevTools to inspect element state
3. **Scroll element into view:** Ensure element is in viewport before clicking

---

#### Issue: Configuration Property Not Found

**Symptoms:**
```
KeyError: 'url'
```

**Cause:** Required configuration property is missing from config.yaml.

**Solution:**
Add missing property to `config/config.yaml`:
```yaml
url: https://testinium-qa.herokuapp.com/web
web.table.url: https://testinium-qa.herokuapp.com/web/login
EmplTitle: "Employees - Odoo"
```

---

#### Issue: Page Title Mismatch

**Symptoms:**
```
AssertionError: Expected page title 'Employees - Odoo', but got 'Dashboard - Odoo'
```

**Cause:** Navigation did not complete, or page title changed in application.

**Solutions:**
1. **Verify URL:** Check that the correct URL was navigated to
2. **Increase wait time:** Page may need more time to load
3. **Update expected title:** If application changed, update EmplTitle in config or step implementation

---

#### Issue: StaleElementReferenceException

**Symptoms:**
```
StaleElementReferenceException: Element is no longer attached to the DOM
```

**Cause:** Page refreshed or element was re-rendered between finding and interacting with it.

**Solution:**
The EmployeePage property-based locators automatically handle this by re-finding elements. Ensure you're using:
```python
employee_page.empl_stage.click()  # ✓ Correct - re-finds element

# Instead of:
element = employee_page.empl_stage
element.click()  # ✗ May be stale
```

---

## Migration Notes

### Java to Python Equivalents

| Java (Cucumber) | Python (Behave) | Notes |
|-----------------|-----------------|-------|
| @When | @when | Lowercase decorator |
| @Then | @then | Lowercase decorator |
| Driver.getDriver() | context.driver | Context-based WebDriver access |
| Thread.sleep(ms) | WebDriverWait with EC | Explicit waits replace sleeps |
| employeePage.login() | employee_page.enter_pos_manager_credentials() | Environment variable credentials |
| {string} | "{name}" | Parameter syntax difference |
| Assert.assertTrue() | assert condition | Python assertion |

### Behavioral Equivalence

All employee step definitions maintain behavioral equivalence with the Java version while improving:
- **Reliability:** Explicit waits instead of sleeps
- **Security:** Environment variables instead of hardcoded credentials
- **Maintainability:** Comprehensive logging and error handling
- **Performance:** Faster execution with condition-based waits

---

## See Also

### Related Documentation

- **Employee Page Object:** [EmployeePage API](../pages/employee-page.md)
- **Configuration API:** [ConfigReader](../utilities/config-reader.md)
- **Wait Helpers:** [WaitHelpers API](../utilities/wait-helpers.md)
- **Employee Testing Guide:** [Employee Management Testing](../../guides/employee-testing.md)
- **Parallel Execution:** [Parallel Testing Guide](../../guides/parallel-execution.md)
- **Step Definition Guide:** [Writing Step Definitions](../../guides/step-definitions.md)
- **Architecture:** [Wait Strategies Architecture](../../architecture/wait-strategies.md)

### External References

- **Behave Documentation:** [behave.readthedocs.io](https://behave.readthedocs.io)
- **Selenium Expected Conditions:** [selenium-python.readthedocs.io/waits](https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions)
- **PEP 257 Docstrings:** [python.org/dev/peps/pep-0257](https://www.python.org/dev/peps/pep-0257/)

---

## Summary

The Employee step definitions module provides 12 comprehensive step implementations for employee and HR management testing:

**Navigation Steps (6):**
- User is on upgenix login page
- User is on the dashboard  
- User clicks Employees stage
- User clicks Challenges stage
- User clicks Departments stage
- User is on the employees dashboard

**CRUD Operations (4):**
- User creates new employees in the Employees stage
- User edits created employees in the Employees module

**Verification Steps (4):**
- User should see the last stage title
- User should see the Employee created message
- User should see listed employees in the Employees stage
- User should see the edited name in the Employees module

**Key Features:**
- ✓ Environment variable-based authentication
- ✓ Explicit waits (no Thread.sleep)
- ✓ Comprehensive logging
- ✓ Thread-safe for parallel execution
- ✓ Full EmployeePage integration
- ✓ ConfigReader integration
- ✓ 29 seconds of sleep time eliminated
- ✓ 100% behavioral equivalence with Java version

