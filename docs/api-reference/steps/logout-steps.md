# Logout Step Definitions API

## Overview

The `logout_steps.py` module provides Behave step definitions for user session termination and logout workflow testing in the Testinium test automation framework. This module implements 3 step definitions that map Gherkin scenarios from `Logout.feature` to executable Python code.

**Module Purpose:**
- Execute logout workflows with popup menu interaction
- Verify login page redirection after logout
- Test back button navigation security after session termination
- Validate session cleanup and re-authentication requirements

**Key Features:**
- Two-step logout workflow (user menu → logout button)
- Login page redirect verification with title validation
- Security testing for browser back button after logout
- Thread-safe driver access through Behave context
- Property-based element locators with explicit waits

**Source:** `features/steps/logout_steps.py`

---

## Module Information

| Property | Value |
|----------|-------|
| **Module Name** | `logout_steps` |
| **Package** | `features.steps` |
| **Framework** | Behave (Python BDD) |
| **Decorators Used** | `@when`, `@then` |
| **Dependencies** | `behave`, `pages.logout_page.LogoutPage` |
| **Step Count** | 3 step definitions |
| **Feature File** | `features/Logout.feature` |
| **Jira Tags** | `@UPGN-291`, `@UPGN-292` |

**Migration Context:**
- **Migrated From:** `src/main/java/com/testinium/step_definitions/LogOutSD.java`
- **Original Framework:** Cucumber (Java)
- **Migration Date:** 2024
- **Key Improvements:** Thread-safe driver access, property-based locators, eliminated hardcoded waits

---

## Step Definitions

### 1. User click Log out option

**Decorator:** `@when('User click Log out option')`

**Function Signature:**
```python
def user_clicks_logout_option(context)
```

**Description:**

Performs the complete two-step logout workflow by interacting with the user menu dropdown and clicking the logout link. This step definition implements the core logout action that terminates the user's authenticated session.

**Workflow Steps:**
1. Click the user menu popup button to expand the dropdown
2. Click the "Log out" link within the expanded dropdown menu

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `context` | `behave.runner.Context` | Yes | Behave context object containing WebDriver instance and shared state |

**Context Attributes Used:**
- `context.driver` - WebDriver instance for browser automation

**Page Objects Used:**
- `LogoutPage(context.driver)` - Provides popup_button and logout_button properties

**Returns:** `None`

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If popup_button or logout_button not clickable within configured timeout |
| `WebDriverException` | If click operations fail due to browser issues |
| `AttributeError` | If context.driver is not initialized |

**Example Usage:**

```python
# Gherkin scenario
Feature: Logout functionality
  Scenario: User logs out successfully
    Given User is logged in
    When User click Log out option
    Then User should see the login dashboard
```

```python
# Behave execution flow
from behave.runner import Context
from selenium import webdriver

context = Context(runner=None)
context.driver = webdriver.Chrome()

# Navigate to authenticated page
context.driver.get("https://testinium.example.com/dashboard")

# Execute logout step
user_clicks_logout_option(context)
# Result: User menu dropdown opened, logout link clicked
```

**Implementation Details:**

```python
# Initialize LogoutPage with context driver
logout_page = LogoutPage(context.driver)

# Click user menu popup button (includes wait_for_clickable)
logout_page.popup_button.click()

# Click logout button in expanded dropdown (includes wait_for_clickable)
logout_page.logout_button.click()
```

**Migration Notes:**

*Java Version (Cucumber):*
```java
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 3);
wait.until(ExpectedConditions.visibilityOf(logOutP.popUpButton));
logOutP.popUpButton.click();
logOutP.logOutButton.click();
```

*Python Version (Behave):*
```python
logout_page = LogoutPage(context.driver)
logout_page.popup_button.click()  # Wait handled by property
logout_page.logout_button.click()  # Wait handled by property
```

**Key Improvements:**
- Eliminated hardcoded 3-second wait
- Wait logic encapsulated in page object properties
- Thread-safe driver access via context
- More Pythonic implementation

**Source:** `features/steps/logout_steps.py:76-133`

---

### 2. User should see the login dashboard

**Decorator:** `@then('User should see the login dashboard')`

**Function Signature:**
```python
def user_should_see_login_dashboard(context)
```

**Description:**

Validates that the user has been successfully logged out by verifying the browser has redirected to the login page. This step checks the page title to confirm logout completion and proper session termination.

**Verification Logic:**
- Retrieves current browser page title
- Compares with expected login page title: `"Login | Best solution for startups"`
- Asserts exact match with descriptive error message

**What This Step Confirms:**
- Logout action completed successfully
- Server-side session terminated
- Browser redirected to unauthenticated login page
- Login page rendered correctly with expected title

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `context` | `behave.runner.Context` | Yes | Behave context object containing WebDriver instance |

**Context Attributes Used:**
- `context.driver` - WebDriver instance to retrieve current page title

**Returns:** `None`

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `AssertionError` | If actual page title does not match expected login page title |
| `AttributeError` | If context.driver is not initialized |
| `WebDriverException` | If unable to retrieve page title from browser |

**Example Usage:**

```python
# Gherkin scenario
Feature: Logout verification
  Scenario: Verify login page after logout
    Given User is logged in
    When User click Log out option
    Then User should see the login dashboard
```

```python
# Behave execution flow
from behave.runner import Context
from selenium import webdriver

context = Context(runner=None)
context.driver = webdriver.Chrome()

# After logout, user should be on login page
context.driver.get("https://testinium.example.com/web/login")

# Execute verification step
user_should_see_login_dashboard(context)
# Result: Assertion passes if title matches
```

**Implementation Details:**

```python
# Define expected login page title
expected_title = "Login | Best solution for startups"

# Get actual page title from browser
actual_title = context.driver.title

# Validate with descriptive error message
assert actual_title == expected_title, (
    f"Expected login page title '{expected_title}', "
    f"but got '{actual_title}'. Logout may have failed or "
    f"redirected to incorrect page."
)
```

**Expected vs Actual Behavior:**

| State | Expected | Verification |
|-------|----------|--------------|
| **Before Logout** | Dashboard page | Not checked |
| **After Logout** | Login page | Title = "Login \| Best solution for startups" |
| **If Failed** | Unknown page | AssertionError with actual title |

**Migration Notes:**

*Java Version (Cucumber):*
```java
String expectedDashboard = "Login | Best solution for startups";
String actualDashboard = Driver.getDriver().getTitle();
Assert.assertEquals("The title is not same as the expected! ",
                    expectedDashboard, actualDashboard);
```

*Python Version (Behave):*
```python
expected_title = "Login | Best solution for startups"
actual_title = context.driver.title
assert actual_title == expected_title, (
    f"Expected login page title '{expected_title}', "
    f"but got '{actual_title}'. Logout may have failed."
)
```

**Key Improvements:**
- More descriptive assertion error message
- F-string formatting for better readability
- Pythonic assert statements instead of JUnit assertions

**Source:** `features/steps/logout_steps.py:136-198`

---

### 3. User can not click the step back button to go the home page

**Decorator:** `@then('User can not click the step back button to go the home page')`

**Function Signature:**
```python
def user_cannot_navigate_back_after_logout(context)
```

**Description:**

Tests critical security functionality by verifying that users cannot access authenticated pages after logout by using the browser's back button. This step ensures proper session invalidation and prevents unauthorized access to protected resources.

**Security Test Flow:**
1. Navigate back using `browser.back()`
2. Verify a warning message is displayed
3. Confirm the warning prevents access to authenticated pages

**Security Implications:**

This test validates critical security requirements:
- Session hijacking prevention via browser history
- Proper server-side session invalidation
- Protection of sensitive data from unauthorized access
- Compliance with security best practices

**⚠️ Critical Security Note:**

If this test fails (no warning message displayed), it indicates a **serious security vulnerability** where users could access authenticated pages after logout via the browser back button, potentially exposing sensitive data or allowing unauthorized actions.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `context` | `behave.runner.Context` | Yes | Behave context object containing WebDriver instance |

**Context Attributes Used:**
- `context.driver` - WebDriver instance to navigate back and verify warning

**Page Objects Used:**
- `LogoutPage(context.driver)` - Provides warning_message property

**Returns:** `None`

**Raises:**

| Exception | Condition | Security Impact |
|-----------|-----------|-----------------|
| `AssertionError` | Warning message not displayed after back navigation | **CRITICAL** - Security vulnerability detected |
| `TimeoutException` | warning_message element not found within timeout | **CRITICAL** - Missing security mechanism |
| `AttributeError` | context.driver is not initialized | Configuration error |
| `WebDriverException` | Browser navigation fails | Browser or network issue |

**Example Usage:**

```python
# Gherkin scenario
Feature: Logout security
  Scenario: Back button prevention after logout
    Given User is logged in
    When User click Log out option
    And User should see the login dashboard
    Then User can not click the step back button to go the home page
```

```python
# Behave execution flow
from behave.runner import Context
from selenium import webdriver

context = Context(runner=None)
context.driver = webdriver.Chrome()

# User is on login page after logout
context.driver.get("https://testinium.example.com/web/login")

# Execute security test step
user_cannot_navigate_back_after_logout(context)
# Result: Assertion passes if warning message displayed
```

**Implementation Details:**

```python
# Attempt to navigate back (simulate back button click)
context.driver.back()

# Initialize LogoutPage to access warning_message
logout_page = LogoutPage(context.driver)

# Retrieve warning message with explicit wait
warning_element = logout_page.warning_message

# Verify warning is displayed (security check)
assert warning_element.is_displayed(), (
    "Expected warning message to be displayed after back navigation "
    "post-logout, but no warning was found. This indicates a security "
    "vulnerability where users can access authenticated pages after "
    "logout via browser back button."
)
```

**Test Scenarios:**

| Scenario | User Action | Expected Result | Security Status |
|----------|-------------|-----------------|-----------------|
| **Pass** | Click back after logout | Warning message displayed | ✅ Secure |
| **Fail** | Click back after logout | No warning, dashboard accessible | ❌ Vulnerable |

**Migration Notes:**

*Java Version (Cucumber):*
```java
Driver.getDriver().navigate().back();
Assert.assertTrue(logOutP.warningMess.isDisplayed());
```

*Python Version (Behave):*
```python
context.driver.back()
logout_page = LogoutPage(context.driver)
warning_element = logout_page.warning_message
assert warning_element.is_displayed(), (
    "Expected warning message after back navigation post-logout, "
    "but no warning was displayed. Security vulnerability detected."
)
```

**Key Improvements:**
- More descriptive security-focused error message
- Explicit security vulnerability warning in assertion
- Property-based element access with automatic waits

**Source:** `features/steps/logout_steps.py:201-289`

---

## Gherkin-to-Code Mapping

### Feature File: Logout.feature

**Source:** `features/Logout.feature`

#### Scenario 1: Successful Logout

**Gherkin:**
```gherkin
@UPGN-291
Scenario Outline: User logs out and ends up in login page
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  And User should see the dashboard
  And User click Log out option
  Then User should see the login dashboard
  
  @SalesManager
  Examples: SalesManager credentials
    |username               |password    |
    |salesmanager7@info.com |salesmanager|
    |salesmanager8@info.com |salesmanager|
    |salesmanager9@info.com |salesmanager|
  
  @PosManager
  Examples: PosManager credentials
    |username               |password    |
    |posmanager5@info.com   |posmanager  |
    |posmanager6@info.com   |posmanager  |
    |posmanager7@info.com   |posmanager  |
```

**Step Mapping:**
- `When User click Log out option` → `user_clicks_logout_option(context)`
- `Then User should see the login dashboard` → `user_should_see_login_dashboard(context)`

**Test Coverage:** 6 scenarios (3 SalesManager + 3 PosManager)

---

#### Scenario 2: Back Button Security Test

**Gherkin:**
```gherkin
@UPGN-292
Scenario Outline: User cannot return to home page after logout
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  And User should see the dashboard
  And User click Log out option
  And User should see the login dashboard
  Then User can not click the step back button to go the home page
  
  @SalesManager
  Examples: SalesManager credentials
    |username               |password    |
    |salesmanager7@info.com |salesmanager|
    |salesmanager8@info.com |salesmanager|
    |salesmanager9@info.com |salesmanager|
  
  @PosManager
  Examples: PosManager credentials
    |username               |password    |
    |posmanager5@info.com   |posmanager  |
    |posmanager6@info.com   |posmanager  |
    |posmanager7@info.com   |posmanager  |
```

**Step Mapping:**
- `When User click Log out option` → `user_clicks_logout_option(context)`
- `Then User should see the login dashboard` → `user_should_see_login_dashboard(context)`
- `Then User can not click the step back button to go the home page` → `user_cannot_navigate_back_after_logout(context)`

**Test Coverage:** 6 scenarios (3 SalesManager + 3 PosManager)

**Total Scenarios:** 12 logout scenarios across 2 user roles

---

## Context Object Usage

### Behave Context Attributes

The logout step definitions rely on the Behave context object for sharing state across steps:

| Attribute | Type | Source | Usage |
|-----------|------|--------|-------|
| `context.driver` | `selenium.webdriver.remote.webdriver.WebDriver` | `features/environment.py` | WebDriver instance for browser automation |

**Context Initialization:**

The `context.driver` is initialized in `features/environment.py` using the `before_scenario` hook:

```python
def before_scenario(context, scenario):
    """Initialize WebDriver before each scenario."""
    from utilities.driver_manager import DriverManager
    context.driver = DriverManager.get_driver()
```

**Context Cleanup:**

The driver is cleaned up in the `after_scenario` hook:

```python
def after_scenario(context, scenario):
    """Cleanup WebDriver after each scenario."""
    from utilities.driver_manager import DriverManager
    DriverManager.quit_driver()
```

### Thread Safety

**Parallel Execution Support:**

When using parallel execution frameworks (`behave-parallel` or `pytest-xdist`), each scenario receives its own isolated context with an independent driver instance. The `DriverManager` uses `threading.local()` to ensure thread-safe driver management.

**Isolation Guarantee:**
- Each worker thread has its own `context` instance
- Each `context.driver` is independent and thread-local
- No cross-scenario driver contamination

---

## Dependencies

### Python Package Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `behave` | 1.2.6+ | BDD framework providing @when, @then decorators |
| `selenium` | 4.15.2+ | WebDriver automation for browser control |

**Installation:**
```bash
pip install behave>=1.2.6 selenium>=4.15.2
```

### Internal Module Dependencies

| Module | Import | Usage |
|--------|--------|-------|
| `pages.logout_page` | `from pages.logout_page import LogoutPage` | Provides element locators and properties for logout UI elements |

**LogoutPage Properties Used:**
- `popup_button` - User menu popup button element (with wait_for_clickable)
- `logout_button` - Logout link element in dropdown (with wait_for_clickable)
- `warning_message` - Warning message element for back button test (with wait_for_visibility)

### External Dependencies

**Selenium WebDriver:**
- Chrome/ChromeDriver for Chrome browser automation
- Firefox/GeckoDriver for Firefox browser automation
- Edge/EdgeDriver for Edge browser automation

**Configuration:**
- WebDriver paths managed by `webdriver-manager` package
- Browser selection configured in `config/config.yaml`

---

## Best Practices

### Step Definition Best Practices

1. **Exact Step Text Matching:**
   - Step texts MUST match Gherkin feature files exactly (case-sensitive)
   - Changes to step text break test execution
   - Use descriptive step names that explain business action

2. **Context Usage:**
   - Always access driver via `context.driver` for thread safety
   - Store scenario-specific data in context for sharing between steps
   - Never use global variables for driver or state

3. **Wait Strategy:**
   - Use page object properties with built-in explicit waits
   - Avoid `time.sleep()` - use WebDriverWait instead
   - Let page objects handle all wait logic

4. **Error Handling:**
   - Use descriptive assertion messages explaining failure causes
   - Include expected vs actual values in error messages
   - Consider security implications in security test assertions

5. **Page Object Interaction:**
   - Always instantiate page objects with `context.driver`
   - Use property-based element access for automatic waits
   - Don't cache page objects across steps (recreate as needed)

### Security Testing Best Practices

1. **Session Invalidation:**
   - Always test back button navigation after logout
   - Verify warning messages or login redirects
   - Consider forward navigation tests as well

2. **Error Visibility:**
   - Security test failures should be loud and obvious
   - Include "SECURITY VULNERABILITY" in failure messages
   - Document security implications in docstrings

3. **Coverage:**
   - Test multiple user roles (SalesManager, PosManager)
   - Test different logout paths (menu, timeout, etc.)
   - Verify both client and server-side session cleanup

---

## Troubleshooting

### Common Issues

#### Issue 1: TimeoutException on popup_button

**Symptoms:**
```
selenium.common.exceptions.TimeoutException: Message: 
Timed out waiting for popup_button to be clickable
```

**Causes:**
- User menu button not visible on page
- Page not fully loaded before logout attempt
- Element locator changed in application

**Solutions:**
1. Verify user is logged in before logout:
   ```gherkin
   Given User is logged in  # Ensure authenticated state
   When User click Log out option
   ```

2. Check element locator in `LogoutPage`:
   ```python
   # Verify locator matches current application HTML
   _POPUP_BUTTON = (By.XPATH, "//button[@class='user-menu']")
   ```

3. Increase timeout in configuration:
   ```yaml
   # config/config.yaml
   timeouts:
     explicit: 15  # Increase from 10 to 15 seconds
   ```

---

#### Issue 2: AssertionError - Wrong Page Title

**Symptoms:**
```
AssertionError: Expected login page title 'Login | Best solution for startups', 
but got 'Dashboard | Testinium'. Logout may have failed.
```

**Causes:**
- Logout action did not complete successfully
- Server-side session not terminated
- Browser cached authenticated state
- Network delay in redirect

**Solutions:**
1. Add explicit wait for redirect:
   ```python
   from selenium.webdriver.support.ui import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   
   # Wait for URL to change to login page
   WebDriverWait(context.driver, 10).until(
       EC.url_contains("/login")
   )
   ```

2. Verify logout button click succeeded:
   ```python
   # Add logging to verify clicks
   import logging
   logout_page = LogoutPage(context.driver)
   logout_page.popup_button.click()
   logging.info("Popup button clicked")
   logout_page.logout_button.click()
   logging.info("Logout button clicked")
   ```

3. Check for JavaScript errors:
   ```python
   # Capture browser console logs
   logs = context.driver.get_log('browser')
   for log in logs:
       print(log)
   ```

---

#### Issue 3: AssertionError - No Warning Message After Back Navigation

**Symptoms:**
```
AssertionError: Expected warning message to be displayed after back navigation 
post-logout, but no warning was found. This indicates a security vulnerability.
```

**⚠️ Critical Security Issue**

**Causes:**
- **Security Vulnerability:** Application allows authenticated page access after logout
- Server-side session not properly invalidated
- Client-side state not cleared
- Browser cache serving authenticated pages

**Solutions:**

1. **Immediate Action:**
   - Report security vulnerability to development team
   - Document reproduction steps
   - Assess data exposure risk

2. **Server-Side Fix Required:**
   ```python
   # Server must invalidate session and prevent caching
   # HTTP Response Headers should include:
   # Cache-Control: no-cache, no-store, must-revalidate
   # Pragma: no-cache
   # Expires: 0
   ```

3. **Verify Session Token:**
   ```python
   # Check if session cookie is cleared after logout
   cookies = context.driver.get_cookies()
   session_cookie = next((c for c in cookies if c['name'] == 'sessionid'), None)
   assert session_cookie is None, "Session cookie not cleared after logout"
   ```

4. **Temporary Workaround (Not Recommended):**
   ```python
   # Force page reload after back navigation
   context.driver.back()
   context.driver.refresh()  # Force server round-trip
   # Then check for warning message
   ```

---

#### Issue 4: Step Definition Not Found

**Symptoms:**
```
behave.exceptions.StepNotFound: Step "User click Log out option" not found
```

**Causes:**
- Step text mismatch between feature file and step definition
- Step definition module not imported
- Typo in decorator string

**Solutions:**
1. Verify exact step text match (case-sensitive):
   ```python
   # Feature file
   When User click Log out option
   
   # Step definition (must match exactly)
   @when('User click Log out option')
   ```

2. Check step definition module location:
   ```bash
   # Module must be in features/steps/ directory
   features/steps/logout_steps.py
   ```

3. Verify Behave auto-discovery:
   ```bash
   # List discovered steps
   behave --dry-run --no-summary --format=steps
   ```

---

#### Issue 5: Context.driver AttributeError

**Symptoms:**
```
AttributeError: 'Context' object has no attribute 'driver'
```

**Causes:**
- `before_scenario` hook not executed
- DriverManager initialization failed
- WebDriver binary not found

**Solutions:**
1. Verify `environment.py` hooks:
   ```python
   # features/environment.py must have:
   def before_scenario(context, scenario):
       from utilities.driver_manager import DriverManager
       context.driver = DriverManager.get_driver()
   ```

2. Check WebDriver installation:
   ```bash
   # Install webdriver-manager
   pip install webdriver-manager
   
   # Verify ChromeDriver
   chromedriver --version
   ```

3. Check DriverManager initialization:
   ```python
   # Test DriverManager directly
   from utilities.driver_manager import DriverManager
   driver = DriverManager.get_driver()
   print(driver.title)  # Should not raise error
   ```

---

## See Also

### Related API Documentation

- **[LogoutPage API](../pages/logout-page.md)** - Page object providing logout element locators and properties
- **[LoginPage API](../pages/login-page.md)** - Page object for login functionality (pre-logout state)
- **[Login Step Definitions API](./login-steps.md)** - Step definitions for login workflow
- **[BasePage API](../pages/base-page.md)** - Base page object with wait utilities
- **[DriverManager API](../utilities/driver-manager.md)** - WebDriver lifecycle management

### Related Guides

- **[Authentication Testing Guide](../../guides/authentication-testing.md)** - Comprehensive guide to login/logout testing
- **[Step Definitions Guide](../../guides/step-definitions.md)** - Writing and organizing step definitions
- **[Feature Files Guide](../../guides/feature-files.md)** - Writing Gherkin scenarios
- **[Page Object Model Guide](../../guides/page-object-model.md)** - Page object pattern and best practices
- **[Wait Strategies Guide](../../guides/wait-strategies.md)** - Explicit wait patterns and best practices

### Related Reference Documentation

- **[Behave Configuration Reference](../../reference/behave-configuration.md)** - Behave framework configuration options
- **[Configuration Options Reference](../../reference/configuration-options.md)** - Complete configuration reference
- **[Gherkin Syntax Reference](../../reference/gherkin-syntax.md)** - Gherkin language reference

### External Resources

- **[Behave Documentation](https://behave.readthedocs.io/)** - Official Behave framework documentation
- **[Selenium Python Documentation](https://selenium-python.readthedocs.io/)** - Official Selenium Python bindings documentation
- **[Gherkin Reference](https://cucumber.io/docs/gherkin/)** - Official Gherkin language reference

---

## Migration Reference

### Java to Python Equivalence

For teams migrating from Java/Cucumber to Python/Behave, here are the key equivalences:

| Java/Cucumber | Python/Behave | Notes |
|---------------|---------------|-------|
| `@Then` annotation | `@then` decorator | Lowercase decorator in Python |
| `Driver.getDriver()` | `context.driver` | Driver via Behave context |
| `WebDriverWait(driver, 3)` | Page object properties | Wait encapsulated in properties |
| `Assert.assertEquals()` | `assert x == y` | Native Python assertions |
| `Assert.assertTrue()` | `assert condition` | Native Python assertions |
| `logOutP.popUpButton` | `logout_page.popup_button` | Snake_case naming |
| `isDisplayed()` | `is_displayed()` | Snake_case method names |

### Key Migration Improvements

1. **Wait Strategy:** Hardcoded waits eliminated, replaced with property-based explicit waits
2. **Driver Access:** Thread-safe driver access via Behave context
3. **Assertions:** Descriptive Python assert statements with f-string error messages
4. **Naming:** Pythonic snake_case naming conventions
5. **Type Hints:** Python 3.9+ type hints for better IDE support

**Original Java Source:** `src/main/java/com/testinium/step_definitions/LogOutSD.java`

---

**Last Updated:** 2024  
**Framework Version:** 1.0.0  
**Python Version:** 3.9+  
**Behave Version:** 1.2.6+
