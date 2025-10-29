# SessionPage API Reference

## Overview

`SessionPage` is a page object class providing login session management for the Testinium application. It implements the Page Object Model pattern with property-based element locators and explicit waits for stable, maintainable test automation.

This page object provides access to the login form elements including username input, password input, and login submit button. All elements use explicit waits to prevent stale element exceptions and ensure reliable test execution.

**Package:** `pages.session_page`

**Inherits From:** [`BasePage`](base-page.md)

**Source:** `pages/session_page.py`

---

## Class: SessionPage

```python
class SessionPage(BasePage):
    """Session page object for Testinium application login session management."""
```

### Description

SessionPage provides access to login form elements using property-based locators with explicit waits. This class replaces the Java `SessionP.java` implementation which used PageFactory with `@FindBy` annotations. The Python implementation uses private locator constants and `@property` decorators for fresh element references on each access, preventing stale element exceptions.

### Inheritance

```
BasePage (Abstract Base Class)
    ↓
SessionPage
```

SessionPage inherits all wait utilities and element interaction methods from BasePage, including:
- `wait_for_element()` - Wait for element presence
- `wait_for_clickable()` - Wait for element to be clickable
- `wait_for_visibility()` - Wait for element visibility
- `drag_and_drop()` - Drag and drop operations
- `get_elements()` - Find multiple elements

### Attributes

| Attribute | Type | Description | Inherited |
|-----------|------|-------------|-----------|
| `driver` | `WebDriver` | Selenium WebDriver instance for browser automation | Yes |
| `wait` | `WebDriverWait` | Pre-configured WebDriverWait instance with default timeout | Yes |
| `config` | `ConfigReader` | Configuration reader singleton for accessing config.yaml | Yes |
| `default_timeout` | `int` | Default explicit wait timeout in seconds from configuration | Yes |
| `actions` | `ActionChains` | ActionChains for complex interactions (hover, drag-drop) | Yes |
| `logger` | `Logger` | Python logging instance for SessionPage operations | No |

### Locator Constants

SessionPage defines three private locator constants preserved from the Java implementation for behavioral equivalence:

| Constant | Locator Strategy | Value | Purpose |
|----------|-----------------|-------|---------|
| `_INPUT_LOGIN` | By.ID | `"login"` | Username/email input field |
| `_INPUT_PASSWORD` | By.ID | `"password"` | Password input field |
| `_LOGIN_BUTTON` | By.XPATH | `"//button[.='Log in']"` | Login submit button (text-based) |

**Source:** `pages/session_page.py:110-112`

---

## Constructor

### `__init__(driver)`

Initialize SessionPage with WebDriver instance.

```python
def __init__(self, driver) -> None:
    """Initialize SessionPage with WebDriver instance."""
```

#### Description

Replaces Java's `PageFactory.initElements(Driver.getDriver(), this)` pattern with explicit constructor accepting WebDriver instance. Calls BasePage constructor to initialize driver, config, wait, and actions attributes. Also initializes a logger for SessionPage operations.

This constructor establishes the foundation for property-based element access by storing the driver reference and initializing common utilities through BasePage inheritance.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `driver` | `WebDriver` | Yes | Selenium WebDriver instance for browser automation. Expected to be thread-local instance from `DriverManager.get_driver()` supporting parallel test execution with isolated sessions. |

#### Returns

`None` - Constructor initializes instance attributes but returns no value.

#### Example

```python
from selenium import webdriver
from pages.session_page import SessionPage

# Initialize with standard WebDriver
driver = webdriver.Chrome()
session_page = SessionPage(driver)

# Or use thread-local driver from DriverManager (recommended)
from utilities.driver_manager import DriverManager
driver = DriverManager.get_driver()
session_page = SessionPage(driver)
```

**Source:** `pages/session_page.py:114-140`

---

## Properties

SessionPage provides three property-based element accessors. Each property returns a fresh `WebElement` reference with automatic explicit waits, preventing stale element exceptions.

### `input_login`

```python
@property
def input_login(self) -> WebElement:
    """Username/email input field element with automatic presence wait."""
```

#### Description

Returns the username/email input field element with automatic explicit wait for element presence. This property calls `BasePage.wait_for_element()` with the `_INPUT_LOGIN` locator on each access, ensuring a fresh element reference that prevents stale element exceptions.

#### Locator Strategy

- **Strategy:** By.ID
- **Value:** `"login"`
- **Stability:** High - ID-based locator provides fast, stable element identification
- **Origin:** Preserved from Java `@FindBy(id = "login")`

#### Wait Strategy

- **Wait Type:** Element presence (may be visible or hidden but exists in DOM)
- **Wait Method:** `BasePage.wait_for_element()`
- **Default Timeout:** Configured in `config.yaml` at `timeouts.default_explicit_wait`
- **Fallback Timeout:** 10 seconds if configuration missing

#### Returns

| Type | Description |
|------|-------------|
| `WebElement` | Username input field element when present in DOM. Element may be visible or hidden but exists in page structure. |

#### Raises

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If username input field not found within timeout period. Indicates page not loaded or element locator changed. |

#### Example

```python
from utilities.driver_manager import DriverManager
from pages.session_page import SessionPage

# Initialize page object
driver = DriverManager.get_driver()
driver.get("https://app.testinium.com/login")
session_page = SessionPage(driver)

# Property access automatically waits for element presence
username_field = session_page.input_login
username_field.send_keys("user@example.com")
username_field.clear()
username_field.send_keys("different@example.com")

# Verify element attributes
assert session_page.input_login.get_attribute("id") == "login"
assert session_page.input_login.is_displayed()
```

**Source:** `pages/session_page.py:142-180`

---

### `input_password`

```python
@property
def input_password(self) -> WebElement:
    """Password input field element with automatic presence wait."""
```

#### Description

Returns the password input field element with automatic explicit wait for element presence. This property calls `BasePage.wait_for_element()` with the `_INPUT_PASSWORD` locator on each access, ensuring a fresh element reference that prevents stale element exceptions.

#### Locator Strategy

- **Strategy:** By.ID
- **Value:** `"password"`
- **Stability:** High - ID-based locator provides fast, stable element identification
- **Origin:** Preserved from Java `@FindBy(id = "password")`

#### Wait Strategy

- **Wait Type:** Element presence (may be visible or hidden but exists in DOM)
- **Wait Method:** `BasePage.wait_for_element()`
- **Default Timeout:** Configured in `config.yaml` at `timeouts.default_explicit_wait`
- **Fallback Timeout:** 10 seconds if configuration missing

#### Returns

| Type | Description |
|------|-------------|
| `WebElement` | Password input field element when present in DOM. Element may be visible or hidden but exists in page structure. |

#### Raises

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If password input field not found within timeout period. Indicates page not loaded or element locator changed. |

#### Example

```python
from utilities.driver_manager import DriverManager
from pages.session_page import SessionPage

# Initialize page object
driver = DriverManager.get_driver()
driver.get("https://app.testinium.com/login")
session_page = SessionPage(driver)

# Property access automatically waits for element presence
password_field = session_page.input_password
password_field.send_keys("SecurePassword123")
password_field.clear()
password_field.send_keys("UpdatedPassword456")

# Verify element attributes
assert session_page.input_password.get_attribute("type") == "password"
assert session_page.input_password.is_enabled()
```

**Source:** `pages/session_page.py:182-220`

---

### `login_button`

```python
@property
def login_button(self) -> WebElement:
    """Login submit button element with automatic clickable wait."""
```

#### Description

Returns the login submit button element with automatic explicit wait for element clickability. This property calls `BasePage.wait_for_clickable()` with the `_LOGIN_BUTTON` locator on each access, ensuring the button is both visible and enabled before interaction, preventing `ElementNotInteractableException`.

#### Locator Strategy

- **Strategy:** By.XPATH
- **Value:** `"//button[.='Log in']"`
- **Stability:** Medium-High - Text-based XPath locator resilient to structural DOM changes
- **Pattern:** Matches button element with exact text content 'Log in'
- **Origin:** Preserved from Java `@FindBy(xpath="//button[.='Log in']")`

#### Wait Strategy

- **Wait Type:** Element clickability (visible, enabled, not obscured)
- **Wait Method:** `BasePage.wait_for_clickable()`
- **Default Timeout:** Configured in `config.yaml` at `timeouts.default_explicit_wait`
- **Fallback Timeout:** 10 seconds if configuration missing
- **Clickability Checks:**
  - Element is visible in viewport
  - Element is enabled (not disabled)
  - Element is not obscured by other elements

#### Returns

| Type | Description |
|------|-------------|
| `WebElement` | Login button element when clickable (visible and enabled). Ready for immediate `click()` operation. |

#### Raises

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If login button not clickable within timeout period. Indicates page still loading, button disabled, or element locator changed. |

#### Example

```python
from utilities.driver_manager import DriverManager
from pages.session_page import SessionPage

# Initialize page object
driver = DriverManager.get_driver()
driver.get("https://app.testinium.com/login")
session_page = SessionPage(driver)

# Property access automatically waits for button to be clickable
login_btn = session_page.login_button
login_btn.click()

# Verify button is clickable before click
assert session_page.login_button.is_displayed()
assert session_page.login_button.is_enabled()
session_page.login_button.click()

# Button text verification
assert session_page.login_button.text == "Log in"
```

**Source:** `pages/session_page.py:222-264`

---

## Complete Usage Example

### Basic Login Workflow

```python
from utilities.driver_manager import DriverManager
from pages.session_page import SessionPage

# Get thread-local WebDriver instance
driver = DriverManager.get_driver()

# Navigate to login page
driver.get("https://app.testinium.com/login")

# Initialize SessionPage
session_page = SessionPage(driver)

# Perform login with automatic waits
session_page.input_login.send_keys("salesmanager1@testinium.com")
session_page.input_password.send_keys("UserUser")
session_page.login_button.click()

# Wait for navigation (handled by step definitions or explicit wait)
# driver.wait.until(EC.url_contains('/dashboard'))
```

### Using in Behave Step Definition

```python
from behave import given, when, then
from pages.session_page import SessionPage

@given('I am on the login page')
def step_navigate_to_login(context):
    """Navigate to login page."""
    context.driver.get("https://app.testinium.com/login")
    context.session_page = SessionPage(context.driver)

@when('I enter username "{username}" and password "{password}"')
def step_enter_credentials(context, username, password):
    """Enter login credentials."""
    context.session_page.input_login.send_keys(username)
    context.session_page.input_password.send_keys(password)

@when('I click the login button')
def step_click_login(context):
    """Click login button."""
    context.session_page.login_button.click()

@then('I should see the login form')
def step_verify_login_form(context):
    """Verify login form is displayed."""
    assert context.session_page.input_login.is_displayed()
    assert context.session_page.input_password.is_displayed()
    assert context.session_page.login_button.is_displayed()
```

---

## Migration from Java

### Original Java Implementation

SessionPage replaces the Java `SessionP.java` implementation which used Selenium PageFactory pattern.

**Original Java Pattern:**
```java
// SessionP.java - Java PageFactory implementation
public class SessionP {
    @FindBy(id = "login")
    public WebElement inputLogin;
    
    @FindBy(id = "password")
    public WebElement inputPassword;
    
    @FindBy(xpath = "//button[.='Log in']")
    public WebElement loginButton;
    
    public SessionP() {
        PageFactory.initElements(Driver.getDriver(), this);
    }
}
```

### Python Transformation

**Key Changes Applied:**

1. **PageFactory Elimination:**
   - Java: `PageFactory.initElements(Driver.getDriver(), this)`
   - Python: `__init__(self, driver)` with `super().__init__(driver)`

2. **Locator Pattern:**
   - Java: `@FindBy(id='login')` annotations
   - Python: `_INPUT_LOGIN = (By.ID, 'login')` constants

3. **Element Access:**
   - Java: `public WebElement inputLogin` (direct field access)
   - Python: `@property def input_login(self)` (property-based with waits)

4. **Stale Element Prevention:**
   - Java: Elements initialized once at construction (prone to stale references)
   - Python: Elements fetched fresh on each property access with explicit waits

5. **Naming Convention:**
   - Java: camelCase (`inputLogin`, `inputPassword`, `loginButton`)
   - Python: snake_case (`input_login`, `input_password`, `login_button`)

### Locator Preservation

All 3 original locators from `SessionP.java` are preserved exactly for behavioral equivalence:

| Java Locator | Python Locator | Preserved? |
|--------------|----------------|------------|
| `@FindBy(id = "login")` | `(By.ID, "login")` | ✓ Yes |
| `@FindBy(id = "password")` | `(By.ID, "password")` | ✓ Yes |
| `@FindBy(xpath = "//button[.='Log in']")` | `(By.XPATH, "//button[.='Log in']")` | ✓ Yes |

---

## Thread Safety

SessionPage is **thread-safe** when used correctly with thread-local WebDriver instances.

### Thread Safety Guarantees

- **Thread-Local Driver:** Each SessionPage instance is constructed with a thread-local WebDriver from `DriverManager.get_driver()`, ensuring isolated browser sessions per test thread.
- **No Shared State:** SessionPage has no class-level mutable state. All element access is through instance properties that call WebDriver APIs.
- **Property-Based Elements:** Element properties return fresh `WebElement` references on each access, preventing cross-thread contamination.

### Parallel Execution Pattern

```python
# Each test thread gets isolated SessionPage instance
@given('I am on the login page')
def step_impl(context):
    # DriverManager.get_driver() returns thread-local driver
    context.driver = DriverManager.get_driver()
    
    # Each thread has isolated SessionPage instance
    context.session_page = SessionPage(context.driver)
```

### Thread Safety Requirements

1. **Use Thread-Local Driver:** Always construct SessionPage with `DriverManager.get_driver()` for parallel execution
2. **Avoid Shared Instances:** Do not share SessionPage instances across test threads
3. **No Class-Level Mutations:** Do not add class-level mutable attributes to SessionPage

---

## Related Documentation

### API References
- [BasePage API](base-page.md) - Parent class providing wait utilities and element interaction methods
- [LoginPage API](login-page.md) - Alternative login page implementation with additional methods
- [Pages Package Overview](index.md) - Complete Page Object Model documentation

### User Guides
- [Authentication Testing Guide](../../guides/authentication-testing.md) - Login/logout testing workflows
- [Page Object Model Guide](../../guides/page-object-model.md) - Creating custom page objects
- [Wait Strategies Guide](../../guides/wait-strategies.md) - Explicit wait patterns and best practices

### Architecture Documentation
- [Page Object Model Architecture](../../architecture/page-object-model.md) - Property-based locator pattern design
- [Thread Safety Architecture](../../architecture/parallel-execution.md) - Thread-local driver pattern

---

## See Also

- **Source Code:** [`pages/session_page.py`](../../pages/session_page.py)
- **Java Original:** `src/main/java/com/testinium/pages/SessionP.java`
- **Step Definitions:** [`features/steps/session_steps.py`](../steps/session-steps.md)
- **Feature File:** [`features/Session.feature`](../../features/Session.feature)
