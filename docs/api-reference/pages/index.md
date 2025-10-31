# Pages Package - Page Object Model API Reference

## Overview

The `pages` package provides a complete **Page Object Model (POM)** implementation for the Testinium test automation framework. This package contains all page object classes that encapsulate web page elements and interactions, following industry best practices for maintainable and scalable test automation.

**Key Features:**

- **BasePage Foundation**: Abstract base class providing common WebDriver utilities, explicit wait helpers, and element interaction methods
- **11 Page Object Implementations**: Complete coverage of all application modules (Authentication, CRM, Employee Management, Inventory, Calendar, Contacts, Notes, Sales, Session)
- **Property-Based Locator Pattern**: Modern Python approach replacing Java's PageFactory `@FindBy` annotations with properties that return fresh element references
- **Explicit Wait Strategy**: All element interactions use explicit waits (no implicit waits) for predictable, reliable test execution
- **Thread-Safe Design**: Each page object instance tied to specific WebDriver instance, enabling safe parallel test execution
- **Configuration Integration**: Timeout values and settings configurable via `config.yaml`

**Package Location:** `pages/`

**Source:** `pages/__init__.py`, `pages/base_page.py`, `pages/*_page.py`

---

## Package Structure

```
pages/
├── __init__.py          # Package exports and metadata
├── base_page.py         # BasePage abstract base class
│
├── login_page.py        # Authentication: User login
├── logout_page.py       # Authentication: User logout
├── session_page.py      # Authentication: Session management
│
├── calendar_page.py     # Application: Calendar and meetings
├── contacts_page.py     # Application: Contact management
├── crm_page.py          # Application: CRM pipeline
├── employee_page.py     # Application: Employee/HR management
├── inventory_page.py    # Application: Inventory/product management
├── notes_page.py        # Application: Notes management
└── sales_page.py        # Application: Sales/customer management
```

---

## Page Object Classes

### Base Class

#### **BasePage** - [View Documentation](base-page.md)

Abstract base class providing the foundation for all page objects in the framework.

**Responsibilities:**
- Explicit wait helpers (`wait_for_element`, `wait_for_clickable`, `wait_for_visibility`, `wait_for_text`)
- Element interaction methods (`click_element`, `enter_text`, `get_element_text`)
- ActionChains integration for complex interactions (`drag_and_drop`)
- Configuration access via ConfigReader
- Logging capabilities for debugging

**All page objects inherit from BasePage** to ensure consistent wait strategies and eliminate code duplication.

---

### Authentication Pages

#### **LoginPage** - [View Documentation](login-page.md)

User authentication page object handling login form interactions.

**Key Features:**
- Email and password input fields
- Login button interaction
- Dashboard navigation verification
- Error message handling for invalid credentials
- Password masking validation

**Typical Usage:**
```python
from pages import LoginPage

login_page = LoginPage(driver)
login_page.login("user@example.com", "password123")
```

---

#### **LogoutPage** - [View Documentation](logout-page.md)

User session termination page object.

**Key Features:**
- Logout button interaction
- Session cleanup verification
- Navigation to login page after logout

---

#### **SessionPage** - [View Documentation](session-page.md)

Session login management page object.

**Key Features:**
- Session-based authentication
- Session timeout handling
- Multi-session management

---

### Application Module Pages

#### **CalendarPage** - [View Documentation](calendar-page.md)

Calendar and meeting management page object.

**Key Features:**
- Event creation and editing
- Meeting scheduling
- Calendar view navigation (day, week, month)
- Attendee management

---

#### **ContactsPage** - [View Documentation](contacts-page.md)

Contacts management page object for creating, editing, and searching contacts.

**Key Features:**
- Contact creation with full details
- Contact search and filtering
- Contact editing and deletion
- Contact list navigation

---

#### **CrmPage** - [View Documentation](crm-page.md)

CRM pipeline and opportunity management page object.

**Key Features:**
- Opportunity creation and management
- Pipeline stage navigation
- Deal tracking
- Customer relationship workflows

---

#### **EmployeePage** - [View Documentation](employee-page.md)

Employee and HR management page object.

**Key Features:**
- Employee CRUD operations (Create, Read, Update, Delete)
- Employee search and filtering
- HR data management
- Employee record validation

---

#### **InventoryPage** - [View Documentation](inventory-page.md)

Inventory and product management page object.

**Key Features:**
- Product creation and management
- Stock level tracking
- Inventory search and filtering
- Product categorization

---

#### **NotesPage** - [View Documentation](notes-page.md)

Notes management page object for creating and organizing notes.

**Key Features:**
- Note creation and editing
- Note categorization
- Note search
- Rich text formatting support

---

#### **SalesPage** - [View Documentation](sales-page.md)

Sales and customer management page object.

**Key Features:**
- Order creation and fulfillment
- Customer information management
- Sales pipeline tracking
- Quote and invoice generation

---

## Page Object Model Pattern

### Property-Based Locator Strategy

The Python implementation uses a **property-based locator pattern** for element access, replacing Java's PageFactory `@FindBy` annotations. This approach provides:

1. **Fresh Element References**: Properties always return current elements, preventing `StaleElementReferenceException`
2. **Built-in Waits**: Element access automatically includes explicit waits
3. **Cleaner Syntax**: Pythonic property access instead of field annotations
4. **Better IDE Support**: Type hints and autocomplete for element properties

**Pattern Example:**

```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    """Login page object with property-based locators."""
    
    # Define locators as class-level tuples (By strategy, locator value)
    _INPUT_EMAIL = (By.NAME, "login")
    _INPUT_PASSWORD = (By.NAME, "password")
    _BUTTON_LOGIN = (By.XPATH, "//button[text()='Giriş Yap']")
    _DASHBOARD = (By.XPATH, "//div[contains(@class, 'dashboard')]")
    
    # Define properties that call BasePage wait methods
    @property
    def input_email(self):
        """Email input field - waits for element to be present."""
        return self.wait_for_element(self._INPUT_EMAIL)
    
    @property
    def input_password(self):
        """Password input field - waits for element to be present."""
        return self.wait_for_element(self._INPUT_PASSWORD)
    
    @property
    def login_button(self):
        """Login button - waits for element to be clickable."""
        return self.wait_for_clickable(self._BUTTON_LOGIN)
    
    # Business logic methods use properties
    def login(self, username: str, password: str):
        """Perform login with credentials.
        
        Args:
            username (str): User email address
            password (str): User password
        """
        self.input_email.send_keys(username)
        self.input_password.send_keys(password)
        self.login_button.click()
```

**Benefits:**

- **No Stale Elements**: Each property call locates element freshly
- **Explicit Waits Included**: Properties use `wait_for_element` or `wait_for_clickable`
- **Readable Tests**: Natural property access: `login_page.input_email.send_keys("test@example.com")`
- **Type Safety**: Type hints on properties improve IDE support

---

### Explicit Wait Strategy

All page objects follow an **explicit wait only** strategy:

**Wait Methods Available (from BasePage):**

| Method | Purpose | When to Use |
|--------|---------|-------------|
| `wait_for_element(locator, timeout)` | Wait for element presence in DOM | General element access |
| `wait_for_clickable(locator, timeout)` | Wait for element to be clickable | Buttons, links, interactive elements |
| `wait_for_visibility(locator, timeout)` | Wait for element to be visible | Elements that may be hidden initially |
| `wait_for_text(locator, text, timeout)` | Wait for element to contain text | Validation, dynamic content |

**No Implicit Waits**: The framework does NOT use implicit waits to avoid unpredictable behavior and timing conflicts.

**Configurable Timeouts**: Default timeout configured in `config.yaml` under `timeouts.default_explicit_wait` (default: 10 seconds).

---

## Usage Examples

### Basic Page Object Usage

```python
from utilities.driver_manager import DriverManager
from pages import LoginPage

# Get WebDriver instance
driver = DriverManager.get_driver()

# Navigate to login page
driver.get("https://example.testinium.com")

# Create page object instance
login_page = LoginPage(driver)

# Interact with page elements
login_page.input_email.send_keys("user@example.com")
login_page.input_password.send_keys("securePassword123")
login_page.login_button.click()

# Verify navigation to dashboard
assert login_page.dashboard.is_displayed()
```

### Using Page Object Methods

```python
from pages import LoginPage, CrmPage

# Login using helper method
login_page = LoginPage(driver)
login_page.login("user@example.com", "password")

# Navigate to CRM module
crm_page = CrmPage(driver)
crm_page.create_opportunity("New Deal", "Tech Corp", "$50,000")
```

### Package-Level Imports

The package supports multiple import styles:

```python
# Import specific page objects
from pages import LoginPage, CalendarPage, CrmPage

# Import with alias
from pages import LoginPage as LP

# Import all page objects (controlled by __all__)
from pages import *

# Explicit module import
from pages.login_page import LoginPage
```

---

## Migration Notes

### Java to Python Transformation

This package replaces the Java `com.testinium.pages` package structure with significant architectural improvements:

**Java Implementation (PageFactory Pattern):**
```java
public class LoginPage {
    @FindBy(name = "login")
    private WebElement inputEmail;
    
    @FindBy(name = "password")
    private WebElement inputPassword;
    
    public LoginPage(WebDriver driver) {
        PageFactory.initElements(driver, this);
    }
    
    public void enterEmail(String email) {
        inputEmail.sendKeys(email);
    }
}
```

**Python Implementation (Property-Based Pattern):**
```python
class LoginPage(BasePage):
    _INPUT_EMAIL = (By.NAME, "login")
    _INPUT_PASSWORD = (By.NAME, "password")
    
    @property
    def input_email(self):
        return self.wait_for_element(self._INPUT_EMAIL)
    
    @property
    def input_password(self):
        return self.wait_for_element(self._INPUT_PASSWORD)
    
    def login(self, username, password):
        self.input_email.send_keys(username)
        self.input_password.send_keys(password)
```

**Key Improvements:**

1. **No Stale Elements**: Properties return fresh elements on each access
2. **Built-in Waits**: Explicit waits integrated into element access
3. **No PageFactory Overhead**: Direct locator usage without reflection/annotation processing
4. **Better Pythonic**: Uses Python decorators instead of Java annotations
5. **Thread Safety**: Property-based approach naturally thread-safe with threading.local() drivers

---

## Package Metadata

**Version:** 1.0.0

**Author:** Blitzy Platform - Test Automation Team

**Migration Source:** `com.testinium.pages` (Java)

**Framework Stack:** Python 3.9+ | Selenium 4.x | Behave BDD

**Design Patterns:**
- Page Object Model (POM)
- Property-based locators
- Explicit wait strategy
- Inheritance for code reuse

---

## Complete API Reference

Explore detailed documentation for each page object:

### Base Class
- **[BasePage](base-page.md)** - Abstract base class with wait helpers and element interaction methods

### Authentication Pages
- **[LoginPage](login-page.md)** - User authentication and login
- **[LogoutPage](logout-page.md)** - User logout and session termination
- **[SessionPage](session-page.md)** - Session management

### Application Module Pages
- **[CalendarPage](calendar-page.md)** - Calendar and meeting management
- **[ContactsPage](contacts-page.md)** - Contact management
- **[CrmPage](crm-page.md)** - CRM pipeline and opportunities
- **[EmployeePage](employee-page.md)** - Employee and HR management
- **[InventoryPage](inventory-page.md)** - Inventory and product management
- **[NotesPage](notes-page.md)** - Notes management
- **[SalesPage](sales-page.md)** - Sales and customer management

---

## See Also

**Related Documentation:**
- [BasePage Wait Strategies](base-page.md#wait-methods) - Detailed wait method documentation
- [Creating Page Objects Guide](../../guides/page-object-model.md) - Tutorial on creating new page objects
- [Parallel Execution Guide](../../guides/parallel-execution.md) - Thread safety considerations
- [Configuration Management](../../guides/configuration-management.md) - Timeout configuration

**Architecture Documentation:**
- [Page Object Model Architecture](../../architecture/page-object-model.md) - Design decisions and patterns
- [Wait Strategies Architecture](../../architecture/wait-strategies.md) - Explicit wait pattern explanation

**Source Code:**
- `pages/__init__.py` - Package exports and metadata
- `pages/base_page.py` - BasePage implementation

---

## Thread Safety Considerations

**Thread-Safe Page Object Usage:**

Page objects are thread-safe when used with thread-local WebDriver instances (provided by `DriverManager.get_driver()`):

```python
# In parallel test execution (behave-parallel or pytest-xdist)
from utilities.driver_manager import DriverManager
from pages import LoginPage

def test_login_parallel():
    # Each thread gets its own WebDriver via threading.local()
    driver = DriverManager.get_driver()
    
    # Each thread gets its own LoginPage instance
    login_page = LoginPage(driver)
    
    # Safe to execute in parallel - no shared state
    login_page.login("user@example.com", "password")
```

**Key Points:**
- Each page object instance has its own `driver` reference
- No shared class-level state that could cause race conditions
- Properties return fresh elements each time, preventing conflicts
- BasePage wait methods are instance-based, not static

**For detailed information**, see [Parallel Execution Guide](../../guides/parallel-execution.md).

---

## Troubleshooting

### Common Issues

#### Issue: StaleElementReferenceException

**Symptoms:** `StaleElementReferenceException: element is not attached to the page document`

**Cause:** Trying to reuse an element reference after page DOM has changed

**Solution:** Use property-based locators - they automatically re-locate elements on each access
```python
# ❌ Bad: Storing element reference
email_input = login_page.input_email
email_input.clear()  # May be stale if page refreshed
email_input.send_keys("new@example.com")

# ✅ Good: Use property each time
login_page.input_email.clear()
login_page.input_email.send_keys("new@example.com")
```

---

#### Issue: TimeoutException waiting for element

**Symptoms:** `TimeoutException: Message: Element not found within timeout`

**Cause:** Element locator incorrect, element not present, or timeout too short

**Solution:**
1. Verify locator is correct using browser DevTools
2. Increase timeout if element legitimately takes longer to appear
3. Check element is in correct iframe context

```python
# Increase timeout for slow-loading element
element = self.wait_for_element(locator, timeout=30)

# Check if element is in iframe
driver.switch_to.frame("iframe_name")
element = self.wait_for_element(locator)
driver.switch_to.default_content()
```

---

#### Issue: Element not clickable / Element is obscured

**Symptoms:** `ElementClickInterceptedException: element click intercepted`

**Cause:** Another element (overlay, modal, loading spinner) is covering the target element

**Solution:** Use `wait_for_clickable` instead of `wait_for_element`
```python
# ✅ Waits for element to be clickable (not obscured)
button = self.wait_for_clickable(self._BUTTON_SUBMIT)
button.click()
```

---

For more troubleshooting guidance, see:
- [Wait Strategies Guide](../../guides/wait-strategies.md)
- [Common Errors Reference](../../troubleshooting/common-errors.md)
- [WebDriver Issues](../../troubleshooting/webdriver-issues.md)

---

**Last Updated:** 2024 | **Framework Version:** 1.0.0
