# LogoutPage API Reference

## Overview

The `LogoutPage` class provides a Page Object Model implementation for user session termination functionality in the Testinium test automation framework. It encapsulates logout-related UI elements and interaction methods following the property-based locator pattern with explicit waits.

**Module:** `pages.logout_page`

**Source:** `pages/logout_page.py`

**Inherits From:** [`BasePage`](base-page.md)

## Key Features

- **Property-based element access** with explicit waits preventing stale element exceptions
- **User menu popup interaction** for accessing logout controls
- **Logout button access** with clickable verification
- **Warning message dialog detection** for handling unsaved changes alerts
- **Complete logout workflow encapsulation** in a single method call
- **Thread-safe** when used with thread-local WebDriver instances

## Migration Context

This class was migrated from the Java `LogOutP.java` Page Object which used PageFactory with `@FindBy` annotations:

**Original Java Implementation:**
```java
@FindBy(className = "o_user_menu") 
public WebElement popUpButton

@FindBy(xpath = "//a[.='Log out']") 
public WebElement logOutButton

@FindBy(xpath = "//div[@class= 'o_dialog_warning modal-body']")
public WebElement warningMess
```

The Python implementation replaces public `WebElement` fields with property-based locators that return fresh element references on each access, preventing stale element exceptions and ensuring more reliable test execution.

**Source:** `pages/logout_page.py:15-24`

## Class Definition

```python
class LogoutPage(BasePage):
    """Page Object for logout functionality in Testinium application."""
```

**Source:** `pages/logout_page.py:61`

## Initialization

### `__init__(driver)`

Initialize LogoutPage with a WebDriver instance.

**Signature:**
```python
def __init__(self, driver: WebDriver) -> None
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `driver` | `WebDriver` | Yes | Selenium WebDriver instance for browser automation. Expected to be a thread-local instance from DriverManager. |

**Example:**
```python
from selenium import webdriver
from pages.logout_page import LogoutPage

driver = webdriver.Chrome()
logout_page = LogoutPage(driver)
# logout_page ready for element interactions
```

**Source:** `pages/logout_page.py:122-144`

## Attributes

### Inherited Attributes

The following attributes are inherited from `BasePage`:

| Attribute | Type | Description |
|-----------|------|-------------|
| `driver` | `WebDriver` | Selenium WebDriver instance for browser automation |
| `config` | `ConfigReader` | Configuration reader singleton for accessing test settings |
| `default_timeout` | `int` | Default explicit wait timeout in seconds |
| `wait` | `WebDriverWait` | Pre-configured WebDriverWait instance |
| `actions` | `ActionChains` | ActionChains instance for complex interactions |

## Element Properties

### `popup_button`

User menu dropdown trigger button property.

**Signature:**
```python
@property
def popup_button(self) -> WebElement
```

**Returns:**

| Type | Description |
|------|-------------|
| `WebElement` | The user menu popup button element ready for clicking |

**Locator Strategy:**
- **Type:** `By.CLASS_NAME`
- **Value:** `'o_user_menu'`
- **Original Java:** `@FindBy(className = "o_user_menu")`

**Wait Strategy:**

Uses `wait_for_clickable()` to ensure the button is:
- Present in DOM
- Visible on screen
- Enabled for interaction
- Not obscured by other elements

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If button not clickable within default timeout (usually indicates page not fully loaded or element hidden) |

**Example:**
```python
from pages.logout_page import LogoutPage
from utilities.driver_manager import DriverManager

driver = DriverManager.get_driver()
driver.get("https://testinium.example.com/dashboard")
logout_page = LogoutPage(driver)

# Access popup button
popup = logout_page.popup_button
popup.click()  # Opens user menu dropdown

# Verify button is displayed
assert logout_page.popup_button.is_displayed()
```

**Source:** `pages/logout_page.py:146-182`

---

### `logout_button`

Logout link within the user menu dropdown property.

**Signature:**
```python
@property
def logout_button(self) -> WebElement
```

**Returns:**

| Type | Description |
|------|-------------|
| `WebElement` | The logout link element ready for clicking |

**Locator Strategy:**
- **Type:** `By.XPATH`
- **Value:** `"//a[.='Log out']"`
- **Original Java:** `@FindBy(xpath = "//a[.='Log out']")`
- **Note:** Text-based XPath provides resilience to DOM structure changes

**Wait Strategy:**

Uses `wait_for_clickable()` to ensure the logout link is:
- Present in DOM (menu dropdown expanded)
- Visible in dropdown menu
- Enabled for interaction
- Ready to trigger logout action

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If logout button not clickable within default timeout (usually indicates dropdown not expanded or page navigation issue) |

**Example:**
```python
from pages.logout_page import LogoutPage

logout_page = LogoutPage(driver)
logout_page.popup_button.click()  # First expand menu

# Access logout button
logout_link = logout_page.logout_button
logout_link.click()  # Trigger logout action

# Verify button text
assert logout_page.logout_button.text == "Log out"
```

**Source:** `pages/logout_page.py:184-222`

---

### `warning_message`

Optional warning dialog displayed during logout property.

**Signature:**
```python
@property
def warning_message(self) -> WebElement
```

**Returns:**

| Type | Description |
|------|-------------|
| `WebElement` | The warning message dialog element |

**Locator Strategy:**
- **Type:** `By.XPATH`
- **Value:** `"//div[@class='o_dialog_warning modal-body']"`
- **Original Java:** `@FindBy(xpath = "//div[@class= 'o_dialog_warning modal-body']")`
- **Note:** Class-based XPath for modal dialog body

**Wait Strategy:**

Uses `wait_for_visibility()` to ensure the warning dialog is:
- Present in DOM
- Visible on screen (modal displayed)
- Has dimensions (not hidden)
- Ready for text extraction or interaction

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If warning message not visible within default timeout. **This is expected behavior** when no warning is displayed. Callers should handle `TimeoutException` for optional warnings. |

**Example:**
```python
from selenium.common.exceptions import TimeoutException
from pages.logout_page import LogoutPage

logout_page = LogoutPage(driver)
logout_page.logout()

# Check for optional warning
try:
    warning = logout_page.warning_message
    print(f"Warning displayed: {warning.text}")
except TimeoutException:
    print("No warning message - logout proceeding normally")

# Assert specific warning text
try:
    warning = logout_page.warning_message
    assert "unsaved changes" in warning.text.lower()
except TimeoutException:
    pass  # No warning is acceptable
```

**Source:** `pages/logout_page.py:224-273`

## Methods

### `logout()`

Perform complete logout workflow.

**Signature:**
```python
def logout(self) -> None
```

**Description:**

This high-level method encapsulates the entire logout process:

1. Click user menu popup button to expand dropdown
2. Wait for logout button to become clickable in dropdown
3. Click logout button to initiate session termination
4. Log completion of logout action

The method handles the two-step logout interaction pattern used in the Testinium application, ensuring each step completes before proceeding.

**Wait Strategy:**

Each element access uses property methods with explicit waits:
- `popup_button`: Waits for user menu button clickability
- `logout_button`: Waits for logout link clickability after dropdown expansion

**Returns:**

| Type | Description |
|------|-------------|
| `None` | No return value |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If `popup_button` or `logout_button` not clickable within timeout |
| `WebDriverException` | If click operations fail due to browser issues |

**Example - Basic Usage:**
```python
from pages.logout_page import LogoutPage
from utilities.driver_manager import DriverManager

driver = DriverManager.get_driver()
driver.get("https://testinium.example.com/dashboard")
logout_page = LogoutPage(driver)

# Perform logout with single method call
logout_page.logout()

# Verify user redirected to login page
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    EC.url_contains("login")
)
```

**Example - Usage in Behave Step Definitions:**
```python
from behave import when
from pages.logout_page import LogoutPage

@when('User logs out')
def user_logs_out(context):
    logout_page = LogoutPage(context.driver)
    logout_page.logout()
```

**Example - Manual Step-by-Step:**
```python
from pages.logout_page import LogoutPage

logout_page = LogoutPage(driver)

# Manual control over each step
logout_page.popup_button.click()
time.sleep(0.5)  # Optional - wait for dropdown animation
logout_page.logout_button.click()
```

**Source:** `pages/logout_page.py:275-347`

## Thread Safety

`LogoutPage` instances are **thread-safe** when each thread has its own WebDriver instance. This is achieved through:

- **Thread-local WebDriver instances** from `DriverManager.get_driver()` using `threading.local()`
- **Instance isolation** - Each `LogoutPage` instance maintains its own driver reference
- **No shared mutable state** - All element access is through driver-specific queries

This design enables **parallel test execution** where multiple threads can simultaneously perform logout operations without interference.

**Example - Parallel Execution:**
```python
import threading
from utilities.driver_manager import DriverManager
from pages.logout_page import LogoutPage

def test_logout_thread():
    # Each thread gets its own WebDriver
    driver = DriverManager.get_driver()
    driver.get("https://testinium.example.com/dashboard")
    
    logout_page = LogoutPage(driver)
    logout_page.logout()
    
    DriverManager.quit_driver()

# Run multiple threads
threads = [threading.Thread(target=test_logout_thread) for _ in range(3)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
```

**Source:** `pages/logout_page.py:85-87`

## Complete Usage Example

```python
"""
Complete example demonstrating LogoutPage usage in a test scenario.
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage

# Setup
driver = webdriver.Chrome()
driver.get("https://testinium.example.com")

try:
    # Login first
    login_page = LoginPage(driver)
    login_page.login("user@example.com", "password123")
    
    # Wait for dashboard
    WebDriverWait(driver, 10).until(
        EC.url_contains("dashboard")
    )
    
    # Initialize logout page
    logout_page = LogoutPage(driver)
    
    # Perform logout
    logout_page.logout()
    
    # Check for optional warning message
    try:
        warning = logout_page.warning_message
        print(f"Warning: {warning.text}")
        # Handle warning if needed
    except TimeoutException:
        print("No warning displayed")
    
    # Verify redirect to login page
    WebDriverWait(driver, 10).until(
        EC.url_contains("login")
    )
    print("Logout successful - redirected to login page")
    
finally:
    driver.quit()
```

## Element Locators Reference

| Property | Locator Type | Locator Value | Wait Method | Java Equivalent |
|----------|--------------|---------------|-------------|-----------------|
| `popup_button` | `CLASS_NAME` | `'o_user_menu'` | `wait_for_clickable()` | `@FindBy(className = "o_user_menu")` |
| `logout_button` | `XPATH` | `"//a[.='Log out']"` | `wait_for_clickable()` | `@FindBy(xpath = "//a[.='Log out']")` |
| `warning_message` | `XPATH` | `"//div[@class='o_dialog_warning modal-body']"` | `wait_for_visibility()` | `@FindBy(xpath = "//div[@class= 'o_dialog_warning modal-body']")` |

**Source:** `pages/logout_page.py:115-120`

## Design Patterns

### Property-Based Locators

`LogoutPage` uses property-based locators (Python `@property` decorator) instead of direct element storage. This pattern:

- **Prevents stale element exceptions** by fetching fresh element references on each access
- **Integrates explicit waits** automatically through `BasePage` wait methods
- **Provides cleaner API** compared to Java's PageFactory pattern
- **Enables lazy evaluation** - elements are only located when accessed

**Pattern Comparison:**

| Java PageFactory | Python Property-Based |
|------------------|----------------------|
| `@FindBy` annotation | `@property` decorator |
| Element stored in field | Element fetched on access |
| Requires page initialization | Elements located on-demand |
| Prone to stale elements | Fresh references prevent staleness |

### Explicit Waits Only

All element access in `LogoutPage` uses **explicit waits** through `BasePage` methods:

- `wait_for_clickable()` for interactive elements (buttons)
- `wait_for_visibility()` for visual elements (dialogs)
- **No implicit waits** - avoids unpredictable wait behavior
- **Configurable timeouts** through `config.yaml`

**Source:** `pages/logout_page.py:26-31`

## See Also

- **[BasePage API Reference](base-page.md)** - Base class providing wait utilities and common methods
- **[LoginPage API Reference](login-page.md)** - Related authentication page object
- **[SessionPage API Reference](session-page.md)** - Session management page object
- **[User Guide: Authentication Testing](../../guides/authentication-testing.md)** - Complete guide to login/logout testing workflows
- **[Architecture: Page Object Model](../../architecture/page-object-model.md)** - Framework architecture documentation

## Troubleshooting

### Issue: TimeoutException on popup_button

**Symptoms:** `TimeoutException` when accessing `logout_page.popup_button`

**Cause:** User menu button not visible or page not fully loaded

**Solution:**
```python
# Ensure page is fully loaded
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'o_user_menu'))
)

# Then access logout page
logout_page = LogoutPage(driver)
logout_page.logout()
```

### Issue: TimeoutException on logout_button

**Symptoms:** `TimeoutException` when accessing `logout_page.logout_button`

**Cause:** User menu dropdown not expanded before accessing logout button

**Solution:**
```python
# Always click popup_button first
logout_page = LogoutPage(driver)
logout_page.popup_button.click()

# Add explicit wait for dropdown expansion if needed
time.sleep(0.5)

# Then access logout button
logout_page.logout_button.click()

# Or use the logout() method which handles this automatically
logout_page.logout()
```

### Issue: warning_message TimeoutException treated as error

**Symptoms:** Tests fail due to `TimeoutException` on `warning_message`

**Cause:** Warning message is optional and may not always appear

**Solution:**
```python
# Always wrap warning_message access in try-except
from selenium.common.exceptions import TimeoutException

try:
    warning = logout_page.warning_message
    # Handle warning if present
    print(f"Warning: {warning.text}")
except TimeoutException:
    # No warning is normal behavior
    pass
```

---

**Last Updated:** 2024-01-09  
**Framework Version:** 1.0.0  
**Source File:** `pages/logout_page.py`
