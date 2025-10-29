# LoginPage API Reference

## Overview

The `LoginPage` class provides a Page Object Model implementation for user authentication in the Testinium application. It encapsulates element locators and interaction methods for the login workflow, following best practices for maintainable test automation.

**Module:** `pages.login_page`  
**Class:** `LoginPage`  
**Inheritance:** Inherits from `BasePage`  
**Source:** `pages/login_page.py:61-429`

### Key Features

- **Property-based element access** - Fresh WebElement references via explicit waits
- **Deduplication fix** - Consolidated duplicate password field from Java implementation
- **High-level login method** - Encapsulated authentication workflow
- **Thread-safe** - Safe for parallel test execution with thread-local WebDriver
- **Comprehensive logging** - Debug and info level logging for troubleshooting

### Migration Context

This module migrates the Java PageFactory pattern to Python property-based element access, providing improved reliability and maintainability.

**Original Java File:** `src/main/java/com/testinium/pages/LoginP.java`  
**Pattern Migration:** PageFactory with `@FindBy` annotations → Property-based locators with explicit waits

## Class Definition

```python
class LoginPage(BasePage):
    """
    Login page object for Testinium application user authentication.
    
    Provides element locators and interaction methods for the login page.
    """
```

**Source:** `pages/login_page.py:61-429`

### Constructor

#### `__init__(driver)`

Initialize LoginPage with a WebDriver instance.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| driver | WebDriver | Yes | Selenium WebDriver instance for browser automation. Expected to be thread-local instance from DriverManager. |

**Returns:** None

**Example:**

```python
from selenium import webdriver
from pages.login_page import LoginPage

driver = webdriver.Chrome()
driver.get("https://testinium.example.com/login")

login_page = LoginPage(driver)
# login_page.driver, login_page.wait, login_page.config available
```

**Source:** `pages/login_page.py:158-180`

## Element Properties

All element properties use the `@property` decorator and return fresh WebElement references via BasePage wait methods, preventing stale element exceptions.

### `input_email`

Email/username input field element.

```python
@property
def input_email(self) -> WebElement:
```

**Returns:** `WebElement` - Email input element when present in DOM

**Raises:** `TimeoutException` - If element not found within default timeout

**Locator:** `(By.NAME, "login")`

**Java Equivalent:**
```java
@FindBy(name = "login")
public WebElement inputEmail;
```

**Example:**

```python
login_page.input_email.clear()
login_page.input_email.send_keys("user@example.com")
```

**Source:** `pages/login_page.py:185-208`

---

### `input_password`

Password input field element.

```python
@property
def input_password(self) -> WebElement:
```

**Returns:** `WebElement` - Password input element when present in DOM

**Raises:** `TimeoutException` - If element not found within default timeout

**Locator:** `(By.NAME, "password")`

#### ⚠️ Deduplication Note

**CRITICAL FIX:** This property consolidates duplicate password field locators from the original Java implementation:

- **Java Line 16-17:** `@FindBy(name="password") public WebElement inputPassword`
- **Java Line 31-32:** `@FindBy(name="password") public WebElement bulletPass` *(DUPLICATE - REMOVED)*

Both Java fields used identical `@FindBy(name="password")` locator, creating unnecessary duplication. The Python implementation consolidates them into a single `_INPUT_PASSWORD` locator following the technical specification requirement for "deduplication of password field locator" (Section 0.4.3 and 0.5.1).

**Java Equivalent (Consolidated):**
```java
@FindBy(name="password")
public WebElement inputPassword;  // Line 16-17

@FindBy(name="password")
public WebElement bulletPass;  // Line 31-32 [DUPLICATE - CONSOLIDATED]
```

**Example:**

```python
login_page.input_password.clear()
login_page.input_password.send_keys("SecurePassword123")
```

**Source:** `pages/login_page.py:210-237`

---

### `login_button`

Login submit button element.

```python
@property
def login_button(self) -> WebElement:
```

**Returns:** `WebElement` - Login button when clickable

**Raises:** `TimeoutException` - If button not clickable within default timeout

**Locator:** `(By.XPATH, "//button[.='Log in']")`

**Wait Strategy:** Uses `wait_for_clickable()` to ensure button is visible, enabled, and interactable before returning, preventing click failures.

**Java Equivalent:**
```java
@FindBy(xpath = "//button[.='Log in']")
public WebElement button;
```

**Example:**

```python
login_page.login_button.click()
```

**Source:** `pages/login_page.py:239-262`

---

### `reset_password_link`

Reset password link element.

```python
@property
def reset_password_link(self) -> WebElement:
```

**Returns:** `WebElement` - Reset password link when clickable

**Raises:** `TimeoutException` - If link not clickable within default timeout

**Locator:** `(By.XPATH, "//a[.='Reset Password']")`

**Usage:** Navigate to password reset flow when user forgets credentials.

**Java Equivalent:**
```java
@FindBy(xpath = "//a[.='Reset Password']")
public WebElement resetPass;
```

**Example:**

```python
login_page.reset_password_link.click()
# User redirected to password reset page
```

**Source:** `pages/login_page.py:264-287`

---

### `dashboard`

Dashboard element for login success verification.

```python
@property
def dashboard(self) -> WebElement:
```

**Returns:** `WebElement` - Dashboard navbar when visible

**Raises:** `TimeoutException` - If dashboard not visible within default timeout (indicates login failure or redirection issue)

**Locator:** `(By.ID, "oe_main_menu_navbar")`

**Usage:** Verify successful login by confirming dashboard navbar appears after authentication completes.

**Java Equivalent:**
```java
@FindBy(id = "oe_main_menu_navbar")
public WebElement dashboard;
```

**Example:**

```python
login_page.login("user@example.com", "password")

# Verify login succeeded
assert login_page.dashboard.is_displayed()
assert "Dashboard" in driver.title
```

**Source:** `pages/login_page.py:289-316`

---

### `alert_error_message`

Error message alert element for login failure detection.

```python
@property
def alert_error_message(self) -> WebElement:
```

**Returns:** `WebElement` - Alert element when visible

**Raises:** `TimeoutException` - If alert not visible within default timeout (indicates no error occurred - successful login)

**Locator:** `(By.CLASS_NAME, "alert")`

**Usage:** Capture and verify error messages when login fails due to invalid credentials, account issues, or server errors.

**Java Equivalent:**
```java
@FindBy(className = "alert")
public WebElement alertErrorMessage;
```

**Example:**

```python
login_page.login("invalid@example.com", "wrongpassword")

# Capture error message
if login_page.alert_error_message.is_displayed():
    error_text = login_page.alert_error_message.text
    assert "Invalid credentials" in error_text
```

**Source:** `pages/login_page.py:318-346`

## Methods

### `login(username, password)`

Perform complete login workflow with provided credentials.

```python
def login(self, username: str, password: str) -> None:
```

High-level method encapsulating the full authentication process:
1. Clear and enter username in email field
2. Clear and enter password in password field
3. Click login button
4. Wait for page to process login attempt

This method provides a single entry point for authentication, improving test readability and maintainability compared to individual element interactions in step definitions.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| username | str | Yes | User's email address or username. Example: "admin@example.com", "sales_manager" |
| password | str | Yes | User's password (handled securely, not logged) |

**Returns:** None

**Raises:**

| Exception | Condition |
|-----------|-----------|
| TimeoutException | If email input, password input, or login button not found/clickable within timeout |
| Exception | If element interaction fails (e.g., element not interactable) |

**Security Note:** Password parameter is not logged to prevent credential exposure in logs. Only username (non-sensitive) is logged for debugging purposes.

**Examples:**

**Successful Login:**

```python
from pages.login_page import LoginPage

# Perform login
login_page.login("admin@example.com", "SecurePass123")

# Verify login succeeded
assert login_page.dashboard.is_displayed()
```

**Failed Login:**

```python
# Attempt login with invalid credentials
login_page.login("invalid@example.com", "wrongpass")

# Verify error message appears
assert login_page.alert_error_message.is_displayed()
error_text = login_page.alert_error_message.text
print(f"Login failed: {error_text}")
```

**Usage in Behave Step Definition:**

```python
from behave import when
from pages.login_page import LoginPage

@when('User logs in with "{username}" and "{password}"')
def step_login(context, username, password):
    login_page = LoginPage(context.driver)
    login_page.login(username, password)
```

**Source:** `pages/login_page.py:350-429`

## Inherited Attributes and Methods

`LoginPage` inherits from `BasePage`, providing access to:

### Inherited Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| driver | WebDriver | Selenium WebDriver instance |
| config | ConfigReader | Configuration reader for accessing configuration |
| wait | WebDriverWait | WebDriverWait instance with default timeout |
| actions | ActionChains | ActionChains for complex interactions |
| default_timeout | int | Default explicit wait timeout in seconds |

### Inherited Methods

| Method | Description |
|--------|-------------|
| wait_for_element(locator) | Wait for element presence in DOM |
| wait_for_clickable(locator) | Wait for element to be clickable |
| wait_for_visibility(locator) | Wait for element to be visible |
| wait_for_text(locator, text) | Wait for element to contain text |
| click_element(locator) | Click element with explicit wait |
| enter_text(locator, text) | Enter text with explicit wait |
| get_element_text(locator) | Get element text with explicit wait |
| is_element_displayed(locator) | Check if element is displayed |
| drag_and_drop(source, target) | Perform drag and drop operation |

**See Also:** [BasePage API Reference](base-page.md) for complete inherited functionality.

## Thread Safety

`LoginPage` instances are **thread-safe** when each thread uses its own WebDriver instance. This is achieved via `threading.local()` in `DriverManager`, ensuring proper isolation in parallel test execution.

**Parallel Execution Pattern:**

```python
from utilities.driver_manager import DriverManager
from pages.login_page import LoginPage

# Each thread gets its own WebDriver instance
driver = DriverManager.get_driver()  # Thread-local driver
login_page = LoginPage(driver)

# Safe to use in parallel scenarios
login_page.login("user@example.com", "password")

# Cleanup after test
DriverManager.quit_driver()
```

## Complete Usage Example

```python
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Navigate to login page
    driver.get("https://testinium.example.com/login")
    
    # Initialize LoginPage
    login_page = LoginPage(driver)
    
    # Scenario 1: Successful login
    print("Test Case 1: Valid credentials")
    login_page.login("admin@example.com", "SecurePassword123")
    
    # Verify login success
    assert login_page.dashboard.is_displayed(), "Dashboard not displayed after login"
    print("✓ Login successful - dashboard visible")
    
    # Navigate back to login page for next test
    driver.get("https://testinium.example.com/login")
    login_page = LoginPage(driver)
    
    # Scenario 2: Failed login
    print("\nTest Case 2: Invalid credentials")
    login_page.login("invalid@example.com", "wrongpassword")
    
    # Verify error message
    try:
        error_message = login_page.alert_error_message
        assert error_message.is_displayed(), "Error message not displayed"
        print(f"✓ Login failed as expected: {error_message.text}")
    except TimeoutException:
        print("✗ Error message not found")
    
    # Scenario 3: Password reset link
    print("\nTest Case 3: Password reset")
    login_page.reset_password_link.click()
    print("✓ Navigated to password reset page")

finally:
    # Cleanup
    driver.quit()
```

## Common Patterns

### Pattern 1: Login with Credential Verification

```python
def login_with_verification(login_page, username, password):
    """Login and verify success or capture error."""
    login_page.login(username, password)
    
    try:
        # Wait for dashboard (successful login)
        if login_page.dashboard.is_displayed():
            return {"success": True, "message": "Login successful"}
    except TimeoutException:
        pass
    
    try:
        # Check for error message (failed login)
        error_element = login_page.alert_error_message
        if error_element.is_displayed():
            return {"success": False, "message": error_element.text}
    except TimeoutException:
        return {"success": False, "message": "Unknown error"}
```

### Pattern 2: Data-Driven Login Testing

```python
from behave import given, when, then
from pages.login_page import LoginPage

# Gherkin Scenario Outline
"""
Scenario Outline: Login with multiple users
  Given User is on login page
  When User logs in with "<username>" and "<password>"
  Then Login result should be "<expected_result>"

  Examples:
    | username              | password      | expected_result |
    | admin@example.com     | AdminPass123  | success         |
    | user@example.com      | UserPass456   | success         |
    | invalid@example.com   | wrongpass     | failure         |
"""

@when('User logs in with "{username}" and "{password}"')
def step_login(context, username, password):
    login_page = LoginPage(context.driver)
    login_page.login(username, password)

@then('Login result should be "{expected_result}"')
def step_verify_result(context, expected_result):
    login_page = LoginPage(context.driver)
    
    if expected_result == "success":
        assert login_page.dashboard.is_displayed()
    else:
        assert login_page.alert_error_message.is_displayed()
```

### Pattern 3: Environment-Specific Credentials

```python
import os
from pages.login_page import LoginPage

# Load credentials from environment variables
ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin@example.com")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "default_password")

def login_as_admin(driver):
    """Login with admin credentials from environment."""
    driver.get("https://testinium.example.com/login")
    login_page = LoginPage(driver)
    login_page.login(ADMIN_USER, ADMIN_PASS)
    
    # Verify admin dashboard access
    assert login_page.dashboard.is_displayed()
    return login_page
```

## Troubleshooting

### Issue: TimeoutException on input_email or input_password

**Symptoms:** `TimeoutException: Message: Element not found within timeout`

**Cause:** Page not fully loaded or element locator changed

**Solution:**
1. Verify page URL is correct: `https://testinium.example.com/login`
2. Check if login page structure changed (inspect element locators)
3. Increase default timeout in configuration if page loads slowly
4. Ensure WebDriver is properly initialized

```python
# Verify element locators manually
from selenium.webdriver.common.by import By

driver.get("https://testinium.example.com/login")
email_element = driver.find_element(By.NAME, "login")
print(f"Email field found: {email_element is not None}")
```

### Issue: login() method completes but no dashboard or error appears

**Symptoms:** Login workflow executes without exception, but neither dashboard nor error message is displayed

**Cause:** Page redirection issue or application taking longer than timeout

**Solution:**
1. Add explicit wait after login before checking results
2. Check browser console for JavaScript errors
3. Verify network connectivity during test execution
4. Review application logs for server-side errors

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

login_page.login("user@example.com", "password")

# Wait longer for result
wait = WebDriverWait(driver, 30)
try:
    dashboard = wait.until(EC.visibility_of_element_located((By.ID, "oe_main_menu_navbar")))
    print("Dashboard appeared after extended wait")
except TimeoutException:
    print("Dashboard did not appear - check application logs")
```

### Issue: Stale element reference errors

**Symptoms:** `StaleElementReferenceException: Element is no longer attached to DOM`

**Cause:** Page refresh or DOM manipulation between element access

**Solution:** The property-based locator pattern prevents this issue by fetching fresh elements on each access. If you cache element references manually, avoid this:

```python
# ❌ BAD: Caching element reference
email_field = login_page.input_email
email_field.clear()
# Page refresh happens here
email_field.send_keys("user@example.com")  # StaleElementReferenceException!

# ✓ GOOD: Fresh element access each time
login_page.input_email.clear()
# Page refresh happens here
login_page.input_email.send_keys("user@example.com")  # Works correctly
```

### Issue: Password not entered correctly (hidden characters)

**Symptoms:** Login fails with correct credentials, password field appears empty

**Cause:** Timing issue or input field not ready for text entry

**Solution:**
1. Ensure password field is clickable before sending keys
2. Add small explicit wait before password entry
3. Verify password field doesn't have JavaScript validation blocking input

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait for password field to be ready
password_field = login_page.input_password
password_field.click()  # Focus on field
password_field.clear()
password_field.send_keys("password123")

# Verify password was entered (check length, not value for security)
assert len(password_field.get_attribute("value")) > 0, "Password not entered"
```

## Design Patterns

### Property-Based Locator Pattern

The LoginPage class uses property-based locators instead of Java's PageFactory pattern. This provides several advantages:

**Java PageFactory (Old Pattern):**
```java
@FindBy(name = "login")
public WebElement inputEmail;

// Element located once during PageFactory.initElements()
// Can become stale if page refreshes
```

**Python Property-Based (New Pattern):**
```python
@property
def input_email(self) -> WebElement:
    return self.wait_for_element(self._INPUT_EMAIL)

# Element located fresh on each access
# Automatically handles stale elements
# Built-in explicit wait
```

### Encapsulation of Authentication Workflow

The `login()` method encapsulates the multi-step authentication process into a single high-level method:

**Benefits:**
- **Improved readability:** `login_page.login(user, pass)` vs multiple element interactions
- **Maintainability:** Changes to login workflow isolated to one method
- **Reusability:** Same method usable across all test scenarios
- **Logging:** Centralized logging of authentication attempts

## Migration Notes

### Deduplication of Password Field

**Critical Fix:** The original Java implementation had duplicate password field declarations:

```java
// LoginP.java - BEFORE deduplication
@FindBy(name="password")
public WebElement inputPassword;  // Line 16-17

@FindBy(name="password")
public WebElement bulletPass;  // Line 31-32 - DUPLICATE!
```

Both fields referenced the same DOM element using identical locator `name="password"`. This created:
- **Code duplication** - Two references to single element
- **Maintenance burden** - Changes needed in two places
- **Confusion** - Unclear which field to use

**Python Implementation (AFTER deduplication):**

```python
# Single consolidated locator
_INPUT_PASSWORD: Tuple[str, str] = (By.NAME, "password")

@property
def input_password(self) -> WebElement:
    return self.wait_for_element(self._INPUT_PASSWORD)
```

This consolidation was identified as a critical requirement in the technical specification (Section 0.4.3 and 0.5.1) and successfully implemented in the Python migration.

### Pattern Transformations

| Java Pattern | Python Pattern | Benefit |
|--------------|----------------|---------|
| @FindBy annotations | Private locator tuples | More explicit, testable |
| Public WebElement fields | @property methods | Encapsulation, fresh elements |
| PageFactory.initElements() | Not needed | Simpler initialization |
| Implicit waits | Explicit waits only | More reliable, predictable timing |

## See Also

- [BasePage API Reference](base-page.md) - Parent class providing wait utilities and common methods
- [Authentication Testing Guide](../../guides/authentication-testing.md) - Complete guide for testing login workflows
- [Page Object Model Guide](../../guides/page-object-model.md) - Pattern documentation and best practices
- [Wait Strategies Guide](../../guides/wait-strategies.md) - When to use each wait method
- [Login Step Definitions](../steps/login-steps.md) - Behave step definitions using LoginPage
- [Configuration Reference](../../reference/configuration-options.md) - Timeout and browser configuration

## Source Code

**Full Source:** [`pages/login_page.py`](../../pages/login_page.py)  
**Lines:** 1-462  
**Last Updated:** View git history for latest changes

---

*This documentation is auto-generated from source code docstrings and manually enhanced for clarity. For the most current implementation details, always refer to the source code.*
