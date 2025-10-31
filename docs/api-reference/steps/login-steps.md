# Login Step Definitions API Reference

## Overview

The Login Step Definitions module (`features/steps/login_steps.py`) provides Behave step implementations for authentication workflows in the Testinium QA test automation framework. This module contains 9 step definitions that handle user navigation, credential input, login validation, error handling, and password masking verification.

**Module Purpose:** Implement BDD step definitions for Login.feature scenarios covering valid/invalid credential handling, empty field validation, password masking, and keyboard navigation (Enter key) submission.

**Source:** `features/steps/login_steps.py`

**Related Feature File:** `features/Login.feature`

---

## Module Information

| Property | Value |
|----------|-------|
| **Module Path** | `features/steps/login_steps.py` |
| **Step Count** | 9 step definitions |
| **Decorator Types** | @given (1), @when (4), @then (4) |
| **Feature Coverage** | Login.feature scenarios UPGN-286 through UPGN-290 |
| **Thread Safety** | Thread-safe via Behave context and threading.local() WebDriver |
| **Migration Source** | Java: `src/main/java/com/testinium/step_definitions/LoginSD.java` |

---

## Migration Context

This module was converted from Java/Cucumber to Python/Behave with the following architectural improvements:

### Critical Changes Applied

**1. Wait Strategy Fix**
- **Java Issue:** Hardcoded 3-second WebDriverWait: `WebDriverWait wait = new WebDriverWait(Driver.getDriver(),3)`
- **Python Fix:** Uses BasePage's configurable wait utilities through LoginPage properties, eliminating hardcoded timeouts

**2. Context Pattern**
- **Java Pattern:** Instance field `LoginP loginP = new LoginP()` (line 16)
- **Python Pattern:** Behave context-based `LoginPage(context.driver)` for proper test isolation and thread safety in parallel execution

**3. Assertion Migration**
- **Java:** JUnit `Assert.assertEquals()` and `Assert.assertTrue()`
- **Python:** Native `assert` statements with descriptive error messages

**4. Locator Deduplication**
- **Java:** Duplicate password fields (`inputPassword` and `bulletPass` both with `@FindBy(name="password")`)
- **Python:** Consolidated to single `LoginPage.input_password` property

---

## Dependencies

### External Dependencies

```python
from behave import given, when, then  # BDD framework decorators
from selenium.webdriver.common.by import By  # Element locator strategies
```

### Internal Dependencies

```python
from pages.login_page import LoginPage  # Login page object for element interactions
from utilities.config_reader import ConfigReader  # Configuration management
```

### Context Object Usage

All step definitions receive a `context` parameter (Behave context object) providing:

- **context.driver**: Thread-local WebDriver instance from DriverManager
- **context.config**: ConfigReader singleton for configuration access
- **Isolation**: Each scenario receives independent context in parallel execution

---

## Step Definitions

### GIVEN Steps (Preconditions)

#### @given('User is on the upgenix login page')

Navigate to login page using configured URL from config.yaml.

**Function:** `step_navigate_to_login_page(context)`

**Purpose:** Implements the Background step from Login.feature, executed before each scenario to ensure user starts on the login page.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | behave.runner.Context | Behave context object containing driver and configuration |

**Configuration:**
- Retrieves login URL from `config.yaml` via `ConfigReader.get_property('web.table.url')`
- Falls back to `BASE_URL` environment variable if key not found

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `KeyError` | If 'web.table.url' configuration key missing and no default provided |
| `WebDriverException` | If navigation to URL fails |

**Java Equivalent:**
```java
@Given("User is on the upgenix login page")
public void user_is_on_the_upgenix_login_page() {
    String url = ConfigurationReader.getProperty("web.table.url");
    Driver.getDriver().get(url);
}
```

**Example Usage:**
```gherkin
Feature: Testinium app login feature
  Background:
    Given User is on the upgenix login page
```

**Implementation:**
```python
@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    config_reader = ConfigReader()
    login_url = config_reader.get_property('web.table.url')
    context.driver.get(login_url)
```

**Source:** `features/steps/login_steps.py:90-136`

---

### WHEN Steps (Actions)

#### @when('User enters "{username}" username')

Enter username/email into login form email input field.

**Function:** `step_enter_username(context, username)`

**Purpose:** Support parameterized username input from Scenario Outline Examples tables, enabling data-driven testing with multiple user credentials.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | behave.runner.Context | Behave context object containing WebDriver instance |
| `username` | str | Parameterized username value extracted from Gherkin Examples table |

**Example Values:**
- `"salesmanager7@info.com"`
- `"posmanager5@info.com"`
- `"salesm27aners@info.com"` (invalid for testing error scenarios)

**Implementation Details:**
- Instantiates `LoginPage` with `context.driver` for element access
- Uses `LoginPage.input_email` property (waits for element presence)
- Sends keys directly without explicit `clear()` as field is typically empty
- Property-based locator prevents stale element exceptions

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If email input element not found within default timeout |
| `WebDriverException` | If send_keys operation fails |

**Java Equivalent:**
```java
@When("User enters {string} username")
public void user_enters_username(String username) {
    loginP.inputEmail.sendKeys(username);
}
```

**Example Usage:**
```gherkin
Scenario Outline: Users log in with valid credentials
  When User enters "<username>" username
  And User enters "<password>" password
  
  Examples:
    |username               |password    |
    |salesmanager7@info.com |salesmanager|
```

**Source:** `features/steps/login_steps.py:142-186`

---

#### @when('User enters "{password}" password')

Enter password into login form password input field.

**Function:** `step_enter_password(context, password)`

**Purpose:** Support parameterized password input from Scenario Outline Examples tables for testing various password scenarios including valid passwords, invalid passwords, and password masking verification.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | behave.runner.Context | Behave context object containing WebDriver instance |
| `password` | str | Parameterized password value extracted from Gherkin Examples table |

**Example Values:**
- `"salesmanager"` (valid)
- `"saLesManager"` (invalid case sensitivity)
- `"SaLeSMaNaGeR"` (invalid case)

**Security Note:**
Password parameter is not logged in detail to prevent credential exposure in test logs. Only confirmation of action is logged.

**Implementation Details:**
- Uses `LoginPage.input_password` property (consolidated from Java's duplicate fields)
- Original Java had duplicate password fields (`inputPassword` and `bulletPass`)
- Python implementation consolidates to single `input_password` property
- Property returns fresh element reference with explicit wait

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If password input element not found within default timeout |
| `WebDriverException` | If send_keys operation fails |

**Java Equivalent:**
```java
@When("User enters {string} password")
public void user_enters_password(String password) {
    loginP.inputPassword.sendKeys(password);
}
```

**Example Usage:**
```gherkin
Scenario Outline: Users log in with invalid credentials
  When User enters "<username>" username
  And User enters "<password>" password
  
  Examples:
    |username               |password    |
    |salesmanager6@info.com |saLesManager|
```

**Source:** `features/steps/login_steps.py:188-238`

---

#### @when('User clicks the login button')

Click the login button to submit authentication credentials.

**Function:** `step_click_login_button(context)`

**Purpose:** Trigger login form submission, initiating server-side authentication with previously entered username and password.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | behave.runner.Context | Behave context object containing WebDriver instance |

**Implementation Details:**
- Uses `LoginPage.login_button` property with `wait_for_clickable`
- Ensures button is visible, enabled, and interactable before click
- BasePage wait utilities prevent click failures from element not ready
- Click triggers JavaScript form submission and page navigation

**Expected Outcomes:**

| Scenario | Outcome |
|----------|---------|
| Valid credentials | Browser navigates to dashboard (title becomes "Odoo") |
| Invalid credentials | Error message alert appears with validation message |
| Empty field | Browser shows native HTML5 validation message |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If login button not clickable within default timeout |
| `WebDriverException` | If click operation fails or element intercepted |

**Java Equivalent:**
```java
@When("User clicks the login button")
public void user_clicks_the_login_button() {
    loginP.button.click();
}
```

**Example Usage:**
```gherkin
Scenario: Successful login
  When User enters "salesmanager7@info.com" username
  And User enters "salesmanager" password
  And User clicks the login button
  Then User should see the dashboard
```

**Source:** `features/steps/login_steps.py:240-286`

---

#### @when('User clicks the enter button')

Click the login button using Enter key alternative submission method.

**Function:** `step_click_enter_button(context)`

**Purpose:** Verify that Enter key submission works as alternative to mouse click, supporting accessibility and keyboard-only navigation scenarios.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | behave.runner.Context | Behave context object containing WebDriver instance |

**Implementation Note:**
Despite step name suggesting Enter key press, this implementation maintains functional equivalence with Java version which calls `button.click()` directly (Java line 67). Both approaches submit the form successfully.

**Alternative Implementation:**
For true Enter key functionality, could use `send_keys(Keys.ENTER)` on password field:
```python
login_page.input_password.send_keys(Keys.ENTER)
```

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If login button not clickable within default timeout |
| `WebDriverException` | If click operation fails |

**Java Equivalent:**
```java
@When("User clicks the enter button")
public void user_clicks_the_enter_button() {
    loginP.button.click();  // Note: Java also uses button click, not Enter key
}
```

**Example Usage:**
```gherkin
@UPGN-290
Scenario Outline: User tries whether enter button works on the login page
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the enter button
  Then User should see the dashboard
```

**Source:** `features/steps/login_steps.py:288-335`

---

### THEN Steps (Assertions)

#### @then('User should see the dashboard')

Verify successful login by validating dashboard appears and page title is 'Odoo'.

**Function:** `step_verify_dashboard(context)`

**Purpose:** Confirm authentication succeeded by checking:
1. Dashboard element is visible on the page
2. Browser page title matches expected value "Odoo"

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | behave.runner.Context | Behave context object containing WebDriver instance |

**Critical Fix Applied:**
- **Hardcoded Wait Elimination**: Java implementation instantiated hardcoded 3-second WebDriverWait: `WebDriverWait wait = new WebDriverWait(Driver.getDriver(),3)`
- **Python Fix**: Uses `LoginPage.dashboard` property which internally calls `BasePage.wait_for_visibility` with configurable timeout from config.yaml

**Expected State:**
- User successfully authenticated with valid credentials
- Browser navigated to dashboard page (URL changed from login page)
- Dashboard navbar visible with `id="oe_main_menu_navbar"`
- Page title equals "Odoo"

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If dashboard element not visible within default timeout (indicates login failed or page navigation error) |
| `AssertionError` | If page title doesn't match expected "Odoo" (indicates navigation to wrong page) |

**Java Equivalent:**
```java
@Then("User should see the dashboard")
public void user_should_see_the_dashboard() {
    wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
    String expectedDashboard = "Odoo";
    String actualDashboard = Driver.getDriver().getTitle();
    Assert.assertEquals("The title is not same as the expected! ", 
                       expectedDashboard, actualDashboard);
}
```

**Example Usage:**
```gherkin
@UPGN-286
Scenario Outline: Users log in with valid credentials
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  Then User should see the dashboard
```

**Source:** `features/steps/login_steps.py:341-418`

---

#### @then('User sees error message')

Verify error message alert is displayed for invalid login credentials.

**Function:** `step_verify_error_message(context)`

**Purpose:** Confirm authentication failure by checking that error message alert element becomes visible after submitting invalid username/password combination.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | behave.runner.Context | Behave context object containing WebDriver instance |

**Implementation Details:**
- Uses `LoginPage.alert_error_message` property with `wait_for_visibility`
- BasePage wait ensures element appears before assertion
- Error message indicates authentication rejected by server
- Typical error message text: "Wrong login/password"

**Expected State:**
- User submitted invalid credentials (wrong username, wrong password, or both)
- Server rejected authentication attempt
- Error alert element with `class="alert"` visible on page

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If error alert element not visible within default timeout (indicates unexpected success) |
| `AssertionError` | If alert element exists but not displayed (DOM presence without visibility) |

**Java Equivalent:**
```java
@Then("User sees error message")
public void user_sees_error_message() {
    Assert.assertTrue(loginP.alertErrorMessage.isDisplayed());
}
```

**Example Usage:**
```gherkin
@UPGN-287
Scenario Outline: Users log in with invalid credentials
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  Then User sees error message
  
  Examples:
    |username               |password    |
    |salesmanager6@info.com |saLesManager|  # Wrong case
```

**Source:** `features/steps/login_steps.py:420-482`

---

#### @then('User sees "{alert_message}" message')

Verify field validation message matches expected text for empty input fields.

**Function:** `step_verify_validation_message(context, alert_message)`

**Purpose:** Validate browser's native HTML5 field validation messages when required fields are left empty. Parameterized alert_message allows testing different validation messages (e.g., different browser locales).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | behave.runner.Context | Behave context object containing WebDriver instance |
| `alert_message` | str | Expected validation message from Gherkin Examples table |

**Example Values:**
- `"Veuillez renseigner ce champ."` (French: "Please fill out this field")
- `"Please fill out this field."` (English)
- `"このフィールドを入力してください。"` (Japanese)

**Implementation Details:**
- Accesses email input field directly via `context.driver.find_element(By.NAME, "login")`
- Retrieves HTML5 `validationMessage` attribute (browser-native message)
- Compares retrieved message with parameterized expected message
- Supports locale-specific validation messages

**Critical Note:**
Java implementation has assertion order swapped - it asserts `Assert.assertEquals(expectedMessage, alertMessage)` where `expectedMessage` is from browser and `alertMessage` is from test data. Python maintains same functional equivalence.

**Expected State:**
- User clicked login button with empty email field
- Browser triggered HTML5 field validation
- `validationMessage` attribute populated on email input element
- Form submission blocked by browser validation

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `NoSuchElementException` | If email input field not found (element lookup by `name="login"`) |
| `AssertionError` | If validation message doesn't match expected value (indicates different browser locale or validation behavior) |

**Java Equivalent:**
```java
@Then("User sees {string} message")
public void user_sees_please_fill_out_this_field_message(String alertMessage) {
    String expectedMessage = Driver.getDriver()
        .findElement(By.name("login"))
        .getAttribute("validationMessage");
    Assert.assertEquals(expectedMessage, alertMessage);
}
```

**Example Usage:**
```gherkin
@UPGN-288
Scenario Outline: Empty field validation
  When User enters "<password>" username  # Only password, no username
  And User clicks the login button
  Then User sees "Veuillez renseigner ce champ." message
  
  Examples:
    |password    |
    |salesmanager|
```

**Source:** `features/steps/login_steps.py:484-559`

---

#### @then('User should see the password in bullet signs')

Verify password input field masks characters with bullet signs (type="password").

**Function:** `step_verify_password_masking(context)`

**Purpose:** Validate password input field security by confirming the HTML input element has `type="password"` attribute, which causes browsers to display entered characters as bullet signs (•••) or asterisks (***) instead of plain text.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | behave.runner.Context | Behave context object containing WebDriver instance |

**Deduplication Note:**
- **Locator Consolidation**: Java implementation used `bulletPass` field which was duplicate of `inputPassword` field - both with `@FindBy(name="password")`
- **Python Fix**: Uses consolidated `LoginPage.input_password` property eliminating duplication

**Security Implication:**
This test validates important security control - passwords must never be displayed in plain text in input fields. **Failure indicates security vulnerability.**

**Expected State:**
- Password input field present on login page
- Input element HTML: `<input type="password" name="password">`
- Browser renders input as masked bullets/asterisks
- User cannot see actual password characters typed

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If password input element not found within default timeout |
| `AssertionError` | If type attribute doesn't equal "password" (indicates SECURITY ISSUE - password displayed as plain text) |

**Java Equivalent:**
```java
@Then("User should see the password in bullet signs")
public void user_should_see_the_password_in_bullet_signs() {
    Assert.assertTrue(loginP.bulletPass.getAttribute("type").equals("password"));
}
```

**Example Usage:**
```gherkin
@UPGN-289
Scenario Outline: Password masking verification
  When User enters "<password>" password
  Then User should see the password in bullet signs
  
  Examples:
    |password    |
    |saLesManager|
```

**Source:** `features/steps/login_steps.py:561-637`

---

## Gherkin-to-Code Mapping

Complete mapping of Login.feature scenarios to step definition implementations:

### Scenario UPGN-286: Valid Credentials Login

```gherkin
@UPGN-286
Scenario Outline: Users log in with valid credentials
  Given User is on the upgenix login page          # → step_navigate_to_login_page()
  When User enters "<username>" username           # → step_enter_username(context, username)
  And User enters "<password>" password            # → step_enter_password(context, password)
  And User clicks the login button                 # → step_click_login_button(context)
  Then User should see the dashboard               # → step_verify_dashboard(context)
```

**Test Data:** 24 example combinations (13 SalesManager + 11 PosManager credentials)

---

### Scenario UPGN-287: Invalid Credentials Error

```gherkin
@UPGN-287
Scenario Outline: Users log in with invalid email or invalid password
  Given User is on the upgenix login page          # → step_navigate_to_login_page()
  When User enters "<username>" username           # → step_enter_username(context, username)
  And User enters "<password>" password            # → step_enter_password(context, password)
  And User clicks the login button                 # → step_click_login_button(context)
  Then User sees error message                     # → step_verify_error_message(context)
```

**Test Data:** 10 example combinations (5 SalesManager + 5 PosManager invalid credentials)

---

### Scenario UPGN-288: Empty Field Validation

```gherkin
@UPGN-288
Scenario Outline: Users log in with empty email field
  Given User is on the upgenix login page          # → step_navigate_to_login_page()
  When User enters "<password>" username           # → step_enter_username(context, password) [Note: password param used for username]
  And User clicks the login button                 # → step_click_login_button(context)
  Then User sees "Veuillez renseigner ce champ." message  # → step_verify_validation_message(context, "Veuillez renseigner ce champ.")
```

**Test Data:** 2 example combinations (1 SalesManager + 1 PosManager password only)

---

### Scenario UPGN-289: Password Masking

```gherkin
@UPGN-289
Scenario Outline: Password masking verification
  Given User is on the upgenix login page          # → step_navigate_to_login_page()
  When User enters "<password>" password           # → step_enter_password(context, password)
  Then User should see the password in bullet signs  # → step_verify_password_masking(context)
```

**Test Data:** 2 example combinations (1 SalesManager + 1 PosManager password)

---

### Scenario UPGN-290: Enter Key Submission

```gherkin
@UPGN-290
Scenario Outline: Enter button works on login page
  Given User is on the upgenix login page          # → step_navigate_to_login_page()
  When User enters "<username>" username           # → step_enter_username(context, username)
  And User enters "<password>" password            # → step_enter_password(context, password)
  And User clicks the enter button                 # → step_click_enter_button(context)
  Then User should see the dashboard               # → step_verify_dashboard(context)
```

**Test Data:** 6 example combinations (3 SalesManager + 3 PosManager credentials)

---

## Thread Safety and Parallel Execution

### Thread Safety Guarantees

Login step definitions are **thread-safe** when using parallel execution frameworks (`pytest-xdist` or `behave-parallel`) because:

1. **Context Isolation:** Each scenario receives an independent `context` object
2. **Thread-Local WebDriver:** `context.driver` is thread-local via `DriverManager`'s `threading.local()` implementation
3. **Stateless Steps:** Step definitions don't maintain instance state across scenarios
4. **Fresh Page Objects:** Each step instantiates fresh `LoginPage(context.driver)` object

### Parallel Execution Architecture

```
Behave Main Process
├── Worker Thread 1
│   ├── Scenario: Valid Login (salesmanager7)
│   ├── context.driver → threading.local() → Chrome Instance 1
│   └── LoginPage(context.driver) → Independent page object
├── Worker Thread 2
│   ├── Scenario: Invalid Login (salesmanager6)
│   ├── context.driver → threading.local() → Chrome Instance 2
│   └── LoginPage(context.driver) → Independent page object
└── Worker Thread 3
    ├── Scenario: Password Masking
    ├── context.driver → threading.local() → Chrome Instance 3
    └── LoginPage(context.driver) → Independent page object
```

### Configuration for Parallel Execution

**Option 1: pytest-xdist**
```bash
pytest features/steps/login_steps.py -n 4  # 4 parallel workers
```

**Option 2: behave-parallel**
```bash
behave features/Login.feature --processes 4 --parallel-element scenario
```

---

## Complete Usage Examples

### Example 1: Basic Valid Login Test

```gherkin
Feature: Login Authentication
  
  Background:
    Given User is on the upgenix login page
  
  @smoke @UPGN-286
  Scenario: SalesManager logs in successfully
    When User enters "salesmanager7@info.com" username
    And User enters "salesmanager" password
    And User clicks the login button
    Then User should see the dashboard
```

**Execution:**
```bash
behave features/Login.feature --tags=@smoke
```

---

### Example 2: Data-Driven Login Test with Scenario Outline

```gherkin
@UPGN-286
Scenario Outline: Multiple users login with valid credentials
  Given User is on the upgenix login page
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  Then User should see the dashboard
  
  Examples:
    |username               |password    |
    |salesmanager7@info.com |salesmanager|
    |salesmanager8@info.com |salesmanager|
    |posmanager5@info.com   |posmanager  |
    |posmanager6@info.com   |posmanager  |
```

**Execution:**
```bash
behave features/Login.feature --tags=@UPGN-286
```

**Result:** 4 test scenarios executed (one per Examples row)

---

### Example 3: Invalid Credentials Error Handling

```gherkin
@UPGN-287
Scenario: Login fails with wrong password
  Given User is on the upgenix login page
  When User enters "salesmanager7@info.com" username
  And User enters "WrongPassword123" password
  And User clicks the login button
  Then User sees error message
```

**Expected Outcome:** Error alert displayed with "Wrong login/password" message

---

### Example 4: Empty Field HTML5 Validation

```gherkin
@UPGN-288
Scenario: Browser validates empty username field
  Given User is on the upgenix login page
  When User enters "salesmanager" username  # Intentionally using password for username
  And User clicks the login button
  Then User sees "Veuillez renseigner ce champ." message
```

**Expected Outcome:** Browser native validation message appears

---

### Example 5: Password Masking Security Check

```gherkin
@UPGN-289
Scenario: Password field masks input
  Given User is on the upgenix login page
  When User enters "MySecurePassword123!" password
  Then User should see the password in bullet signs
```

**Expected Outcome:** Password field has `type="password"`, characters displayed as •••

---

## Troubleshooting

### Common Issues

#### Issue: "User should see the dashboard" fails with TimeoutException

**Symptoms:** Step times out waiting for dashboard element

**Possible Causes:**
1. Invalid credentials used (wrong username/password)
2. Login button not clicked successfully
3. Network delay in authentication response
4. Dashboard element locator changed in application

**Solutions:**
1. Verify credentials in Examples table match valid test users
2. Check `config.yaml` has correct `web.table.url`
3. Increase explicit wait timeout in `config.yaml`:
   ```yaml
   timeouts:
     explicit: 15  # Increase from 10 to 15 seconds
   ```
4. Verify dashboard element locator `id="oe_main_menu_navbar"` still valid

---

#### Issue: "User sees error message" fails - element not found

**Symptoms:** TimeoutException when verifying error alert

**Possible Causes:**
1. Credentials accidentally valid (should be invalid)
2. Error alert locator changed (`class="alert"`)
3. Application changed error handling behavior

**Solutions:**
1. Verify Examples table has intentionally invalid credentials
2. Check LoginPage.alert_error_message locator still accurate
3. Inspect page HTML after failed login to locate new error element

---

#### Issue: Validation message text doesn't match

**Symptoms:** AssertionError - validation message mismatch

**Possible Causes:**
1. Browser language/locale different from expected
2. Different browser version with different message text

**Solutions:**
1. Set browser locale in configuration:
   ```python
   options.add_experimental_option('prefs', {'intl.accept_languages': 'fr'})
   ```
2. Update Examples table with correct locale message:
   ```gherkin
   Then User sees "Please fill out this field." message  # English
   # Instead of: "Veuillez renseigner ce champ."  # French
   ```

---

#### Issue: Password masking test fails - type is "text" not "password"

**Symptoms:** AssertionError indicating SECURITY ISSUE

**Possible Causes:**
1. Application changed password field to text field (security vulnerability!)
2. Wrong element being tested
3. JavaScript dynamically changing field type

**Solutions:**
1. **Critical:** Report as security vulnerability immediately
2. Verify LoginPage.input_password locator targets correct element
3. Check if application has password visibility toggle feature

---

## See Also

### Related API Documentation
- [LoginPage API Reference](../pages/login-page.md) - Page object for login elements
- [BasePage API Reference](../pages/base-page.md) - Base class with wait utilities
- [DriverManager API Reference](../utilities/driver-manager.md) - Thread-local WebDriver management
- [ConfigReader API Reference](../utilities/config-reader.md) - Configuration access

### Related Guides
- [Authentication Testing Guide](../../guides/authentication-testing.md) - Complete login testing workflows
- [Step Definitions Guide](../../guides/step-definitions.md) - Writing custom step definitions
- [Parallel Execution Guide](../../guides/parallel-execution.md) - Running tests in parallel

### Related References
- [Behave Configuration Reference](../../reference/behave-configuration.md) - Behave settings
- [Configuration Options Reference](../../reference/configuration-options.md) - config.yaml options
- [Gherkin Syntax Reference](../../reference/gherkin-syntax.md) - Writing feature files

### External Documentation
- [Behave Official Documentation](https://behave.readthedocs.io/)
- [Selenium Python Bindings](https://selenium-python.readthedocs.io/)
- [Gherkin Syntax Reference](https://cucumber.io/docs/gherkin/reference/)

---

**Last Updated:** Auto-generated from source code  
**Module Version:** 1.0.0  
**Migration Status:** Complete (from Java/Cucumber LoginSD.java)
