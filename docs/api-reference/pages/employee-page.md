# EmployeePage API Reference

## Overview

The `EmployeePage` class provides a page object for employee and HR management functionality in the Testinium application. This page object implements the Page Object Model pattern with property-based element access, explicit waits, and critical security remediations for credential management.

**Module:** `pages.employee_page`  
**Class:** `EmployeePage`  
**Inherits From:** [`BasePage`](base-page.md)  
**Source:** `pages/employee_page.py`

### Key Features

- **Login Form Access:** Element locators for authentication (email, password, login button)
- **HR Navigation:** Links to Employees, Badges, Challenges, Goals History, and Departments sections
- **Employee Management:** Create, edit, and manage employee records
- **Security Remediation:** Environment variable-based credential management (replaces hardcoded credentials)
- **Property-Based Locators:** Fresh element references with explicit waits prevent stale element exceptions
- **Thread Safety:** Inherits thread-safe WebDriver management from BasePage

### Security Notice

This page object requires `POS_MANAGER_USERNAME` and `POS_MANAGER_PASSWORD` environment variables for authentication. **Never commit credentials to version control.** Use:

- **Development:** `.env` files with python-dotenv
- **CI/CD:** Jenkins Credentials plugin, GitHub Secrets, GitLab CI variables
- **Production:** AWS Secrets Manager, HashiCorp Vault, Azure Key Vault

---

## Class Definition

```python
class EmployeePage(BasePage):
    """Employee page object for Testinium application HR and employee management."""
```

**Source:** `pages/employee_page.py:80-628`

### Constructor

#### `__init__(driver)`

Initialize EmployeePage with a WebDriver instance.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `driver` | `WebDriver` | Yes | Selenium WebDriver instance (typically from `DriverManager.get_driver()`) |

**Example:**

```python
from pages.employee_page import EmployeePage
from utilities.driver_manager import DriverManager

driver = DriverManager.get_driver()
employee_page = EmployeePage(driver)
```

**Source:** `pages/employee_page.py:180-201`

---

## Element Properties

All element properties use the property-based locator pattern with explicit waits, returning fresh `WebElement` references to prevent stale element exceptions.

### Login Form Elements

#### `input_login`

Login email input field.

**Property Type:** `WebElement`  
**Locator:** `(By.ID, 'login')`  
**Wait Strategy:** `wait_for_element()` (element present in DOM)

**Returns:** Login email input field with explicit wait applied

**Example:**

```python
employee_page.input_login.send_keys("user@example.com")
```

**Migration Note:** Converted from Java `@FindBy(id = "login") public WebElement inputLogin;`

**Source:** `pages/employee_page.py:206-223`

---

#### `input_password`

Login password input field.

**Property Type:** `WebElement`  
**Locator:** `(By.ID, 'password')`  
**Wait Strategy:** `wait_for_element()` (element present in DOM)

**Returns:** Login password input field with explicit wait applied

**Example:**

```python
employee_page.input_password.send_keys("securepassword123")
```

**Migration Note:** Converted from Java `@FindBy(id = "password") public WebElement inputPass;`

**Source:** `pages/employee_page.py:224-241`

---

#### `login_button`

Login submit button.

**Property Type:** `WebElement`  
**Locator:** `(By.XPATH, "//button[.='Log in']")`  
**Wait Strategy:** `wait_for_clickable()` (element clickable)

**Returns:** Login button that is clickable with explicit wait applied

**Example:**

```python
employee_page.login_button.click()
```

**Migration Note:** Converted from Java `@FindBy(xpath = "//button[.='Log in']") public WebElement loginButton;`

**Source:** `pages/employee_page.py:242-259`

---

### HR Navigation Elements

#### `empl_stage`

Employees section navigation link.

**Property Type:** `WebElement`  
**Locator:** `(By.PARTIAL_LINK_TEXT, 'Employees')`  
**Wait Strategy:** `wait_for_clickable()` (element clickable)

**Returns:** Employees navigation link that is clickable

**Example:**

```python
# Navigate to Employees section
employee_page.empl_stage.click()
```

**Migration Note:** Converted from Java `@FindBy(partialLinkText = "Employees") public WebElement emplStage;`

**Source:** `pages/employee_page.py:260-277`

---

#### `badges_btn`

Badges section navigation link.

**Property Type:** `WebElement`  
**Locator:** `(By.PARTIAL_LINK_TEXT, 'Badges')`  
**Wait Strategy:** `wait_for_clickable()` (element clickable)

**Returns:** Badges navigation link that is clickable

**Example:**

```python
# Navigate to Badges section
employee_page.badges_btn.click()
```

**Migration Note:** Converted from Java `@FindBy(partialLinkText = "Badges") public WebElement badgesBtn;`

**Source:** `pages/employee_page.py:278-295`

---

#### `challenges_btn`

Challenges section navigation link.

**Property Type:** `WebElement`  
**Locator:** `(By.PARTIAL_LINK_TEXT, 'Challenges')`  
**Wait Strategy:** `wait_for_clickable()` (element clickable)

**Returns:** Challenges navigation link that is clickable

**Example:**

```python
# Navigate to Challenges section
employee_page.challenges_btn.click()
```

**Migration Note:** Converted from Java `@FindBy(partialLinkText = "Challenges") public WebElement challengesBtn;`

**Source:** `pages/employee_page.py:296-313`

---

#### `goals_history_btn`

Goals History section navigation link.

**Property Type:** `WebElement`  
**Locator:** `(By.PARTIAL_LINK_TEXT, 'Goals History')`  
**Wait Strategy:** `wait_for_clickable()` (element clickable)

**Returns:** Goals History navigation link that is clickable

**Example:**

```python
# Navigate to Goals History section
employee_page.goals_history_btn.click()
```

**Migration Note:** Converted from Java `@FindBy(partialLinkText = "Goals History") public WebElement goalsHistoryBtn;`

**Source:** `pages/employee_page.py:314-331`

---

#### `departments_btn`

Departments section navigation link.

**Property Type:** `WebElement`  
**Locator:** `(By.PARTIAL_LINK_TEXT, 'Departments')`  
**Wait Strategy:** `wait_for_clickable()` (element clickable)

**Returns:** Departments navigation link that is clickable

**Example:**

```python
# Navigate to Departments section
employee_page.departments_btn.click()
```

**Migration Note:** Converted from Java `@FindBy(partialLinkText = "Departments") public WebElement departmentsBtn;`

**Source:** `pages/employee_page.py:332-349`

---

### Employee Management Elements

#### `create_btn`

Create new employee button (Kanban board create button).

**Property Type:** `WebElement`  
**Locator:** `(By.XPATH, "//button[@class='btn btn-primary btn-sm o-kanban-button-new btn-default']")`  
**Wait Strategy:** `wait_for_clickable()` (element clickable)

**Returns:** Create employee button that is clickable

**Example:**

```python
# Start creating a new employee
employee_page.create_btn.click()
```

**Migration Note:** Converted from Java `@FindBy(xpath = "//button[@class='btn btn-primary btn-sm o-kanban-button-new btn-default']") public WebElement createBtn;`

**Source:** `pages/employee_page.py:350-368`

---

#### `employees_name`

Employee name input field in creation form.

**Property Type:** `WebElement`  
**Locator:** `(By.XPATH, "//input[@class='o_field_char o_field_widget o_input o_required_modifier']")`  
**Wait Strategy:** `wait_for_element()` (element present in DOM)

**Returns:** Employee name input field with explicit wait applied

**Example:**

```python
# Enter employee name
employee_page.employees_name.send_keys("John Doe")
```

**Migration Note:** Converted from Java `@FindBy(xpath = "//input[@class='o_field_char o_field_widget o_input o_required_modifier']") public WebElement employeesName;`

**Source:** `pages/employee_page.py:369-387`

---

#### `saved_message`

Save button for employee form.

**Property Type:** `WebElement`  
**Locator:** `(By.XPATH, "//button[@class='btn btn-primary btn-sm o_form_button_save']")`  
**Wait Strategy:** `wait_for_clickable()` (element clickable)

**Returns:** Save button that is clickable

**Note:** Despite the name "savedMessage" in the original Java code, this element is actually the save button, not a message element.

**Example:**

```python
# Save employee form
employee_page.saved_message.click()
```

**Migration Note:** Converted from Java `@FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']") public WebElement savedMessage;`

**Source:** `pages/employee_page.py:388-408`

---

#### `created_message`

Employee created confirmation message.

**Property Type:** `WebElement`  
**Locator:** `(By.XPATH, "//p[.='Employee created']")`  
**Wait Strategy:** `wait_for_visibility()` (element visible in viewport)

**Returns:** Confirmation message element with visibility wait

**Example:**

```python
# Verify employee was created successfully
assert "Employee created" in employee_page.created_message.text
```

**Migration Note:** Converted from Java `@FindBy(xpath = "//p[.='Employee created']") public WebElement createdMessage;`

**Source:** `pages/employee_page.py:409-426`

---

#### `choose_employee`

Employee selection element from employee list.

**Property Type:** `WebElement`  
**Locator:** `(By.XPATH, "//html/body/div[1]/div[2]/div[2]/div/div/div/div[1]")`  
**Wait Strategy:** `wait_for_clickable()` (element clickable)

**Returns:** Employee selection element that is clickable

**Note:** This uses an absolute XPath which is brittle. Consider updating to a more stable locator strategy if possible.

**Example:**

```python
# Select an employee from the list
employee_page.choose_employee.click()
```

**Migration Note:** Converted from Java `@FindBy(xpath = "//html/body/div[1]/div[2]/div[2]/div/div/div/div[1]") public WebElement chooseEmployee;`

**Source:** `pages/employee_page.py:427-447`

---

#### `edit_employee`

Edit employee button in employee form.

**Property Type:** `WebElement`  
**Locator:** `(By.XPATH, "//html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/button[1]")`  
**Wait Strategy:** `wait_for_clickable()` (element clickable)

**Returns:** Edit employee button that is clickable

**Note:** This uses an absolute XPath which is brittle. Consider updating to a more stable locator strategy if possible.

**Example:**

```python
# Enter edit mode for selected employee
employee_page.edit_employee.click()
```

**Migration Note:** Converted from Java `@FindBy(xpath = "//html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/button[1]") public WebElement editEmployee;`

**Source:** `pages/employee_page.py:448-468`

---

#### `name_edit`

Employee name edit field (dynamically generated ID).

**Property Type:** `WebElement`  
**Locator:** `(By.XPATH, "//*[@id='o_field_input_678']")`  
**Wait Strategy:** `wait_for_element()` (element present in DOM)

**Returns:** Employee name edit field with explicit wait applied

**Note:** This uses a dynamically generated ID which may change between application versions or sessions. Monitor for stability.

**Example:**

```python
# Update employee name
employee_page.name_edit.clear()
employee_page.name_edit.send_keys("Jane Smith")
```

**Migration Note:** Converted from Java `@FindBy(xpath = "//*[@id='o_field_input_678']") public WebElement nameEdit;`

**Source:** `pages/employee_page.py:469-490`

---

## Methods

### `enter_pos_manager_credentials()`

Enter POS Manager credentials from environment variables and submit login.

```python
def enter_pos_manager_credentials(self) -> None
```

**Parameters:** None

**Returns:** `None`

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `ValueError` | If `POS_MANAGER_USERNAME` or `POS_MANAGER_PASSWORD` environment variables are not set |
| `Exception` | If element interaction fails (e.g., timeout, element not found) |

**Description:**

This method retrieves POS Manager credentials from environment variables and performs the complete login workflow:

1. Retrieves `POS_MANAGER_USERNAME` from environment
2. Retrieves `POS_MANAGER_PASSWORD` from environment
3. Validates both credentials are present (raises `ValueError` if missing)
4. Enters username into `input_login` field
5. Enters password into `input_password` field
6. Clicks `login_button` to submit form

---

### Security Remediation

**CRITICAL:** This method addresses a severe security vulnerability in the original Java implementation.

**Vulnerability in Java (`EmployeeP.java` lines 59-69):**

The original Java code contained hardcoded credentials:

```java
// INSECURE - Original Java implementation
public void enterPosManagerCredentials() {
    inputLogin.sendKeys("posmanager50@info.com");  // Hardcoded username
    inputPass.sendKeys("posmanager");              // Hardcoded password
    loginButton.click();
}

// Even the parameterized version ignored parameters and used hardcoded values
public void enterPosManagerCredentials(String username, String password) {
    inputLogin.sendKeys("posmanager50@info.com");  // BUG: Ignored parameters
    inputPass.sendKeys("posmanager");              // BUG: Ignored parameters
    loginButton.click();
}
```

**Python Security Fix:**

The Python implementation uses environment variables:

```python
# SECURE - Python implementation
def enter_pos_manager_credentials(self) -> None:
    username = os.getenv('POS_MANAGER_USERNAME')
    password = os.getenv('POS_MANAGER_PASSWORD')
    
    if not username or not password:
        raise ValueError("Missing required environment variables")
    
    self.input_login.send_keys(username)
    self.input_password.send_keys(password)
    self.login_button.click()
```

---

### Environment Variable Setup

**Development (using .env file):**

Create a `.env` file in the project root:

```bash
POS_MANAGER_USERNAME=posmanager50@info.com
POS_MANAGER_PASSWORD=posmanager
```

Load with python-dotenv:

```python
from dotenv import load_dotenv
load_dotenv()  # Automatically loads .env file
```

**CI/CD - Jenkins:**

```groovy
pipeline {
    environment {
        POS_MANAGER_USERNAME = credentials('pos-manager-username')
        POS_MANAGER_PASSWORD = credentials('pos-manager-password')
    }
    stages {
        stage('Test') {
            steps {
                sh 'behave features/EmployeeFc.feature'
            }
        }
    }
}
```

**CI/CD - GitHub Actions:**

```yaml
name: Test Employee Features
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Employee Tests
        env:
          POS_MANAGER_USERNAME: ${{ secrets.POS_MANAGER_USERNAME }}
          POS_MANAGER_PASSWORD: ${{ secrets.POS_MANAGER_PASSWORD }}
        run: behave features/EmployeeFc.feature
```

**CI/CD - GitLab CI:**

```yaml
test:employee:
  script:
    - behave features/EmployeeFc.feature
  variables:
    POS_MANAGER_USERNAME: $POS_MANAGER_USERNAME
    POS_MANAGER_PASSWORD: $POS_MANAGER_PASSWORD
```

**Command Line (Unix/Linux/macOS):**

```bash
export POS_MANAGER_USERNAME='posmanager50@info.com'
export POS_MANAGER_PASSWORD='posmanager'
behave features/EmployeeFc.feature
```

**Command Line (Windows):**

```cmd
set POS_MANAGER_USERNAME=posmanager50@info.com
set POS_MANAGER_PASSWORD=posmanager
behave features\EmployeeFc.feature
```

**Production - AWS Secrets Manager:**

```python
import boto3
import os

def load_credentials_from_aws():
    client = boto3.client('secretsmanager')
    secret = client.get_secret_value(SecretId='testinium/pos-manager')
    credentials = json.loads(secret['SecretString'])
    
    os.environ['POS_MANAGER_USERNAME'] = credentials['username']
    os.environ['POS_MANAGER_PASSWORD'] = credentials['password']
```

**Production - HashiCorp Vault:**

```python
import hvac
import os

def load_credentials_from_vault():
    client = hvac.Client(url='https://vault.example.com')
    secret = client.secrets.kv.v2.read_secret_version(path='testinium/pos-manager')
    
    os.environ['POS_MANAGER_USERNAME'] = secret['data']['data']['username']
    os.environ['POS_MANAGER_PASSWORD'] = secret['data']['data']['password']
```

---

### Examples

**Basic Usage:**

```python
import os
from pages.employee_page import EmployeePage
from utilities.driver_manager import DriverManager

# Set environment variables (or load from .env file)
os.environ['POS_MANAGER_USERNAME'] = 'posmanager50@info.com'
os.environ['POS_MANAGER_PASSWORD'] = 'posmanager'

# Initialize page object
driver = DriverManager.get_driver()
driver.get('https://testinium-demo.example.com')

employee_page = EmployeePage(driver)

# Perform login
employee_page.enter_pos_manager_credentials()

# Verify successful login (wait for navigation)
assert "dashboard" in driver.current_url.lower()
```

**Usage with python-dotenv:**

```python
from dotenv import load_dotenv
from pages.employee_page import EmployeePage
from utilities.driver_manager import DriverManager

# Load environment variables from .env file
load_dotenv()

driver = DriverManager.get_driver()
driver.get('https://testinium-demo.example.com')

employee_page = EmployeePage(driver)
employee_page.enter_pos_manager_credentials()
```

**Error Handling:**

```python
from pages.employee_page import EmployeePage
from utilities.driver_manager import DriverManager

driver = DriverManager.get_driver()
driver.get('https://testinium-demo.example.com')

employee_page = EmployeePage(driver)

try:
    employee_page.enter_pos_manager_credentials()
except ValueError as e:
    print(f"Credential configuration error: {e}")
    print("Please set POS_MANAGER_USERNAME and POS_MANAGER_PASSWORD environment variables")
except Exception as e:
    print(f"Login failed: {e}")
    # Take screenshot for debugging
    driver.save_screenshot("login_failure.png")
```

**Source:** `pages/employee_page.py:491-579`

---

## Complete Usage Example

### Employee Creation Workflow

```python
import os
from dotenv import load_dotenv
from pages.employee_page import EmployeePage
from utilities.driver_manager import DriverManager

# Load credentials from .env file
load_dotenv()

# Initialize WebDriver and navigate to application
driver = DriverManager.get_driver()
driver.get('https://testinium-demo.example.com')

# Initialize EmployeePage
employee_page = EmployeePage(driver)

# Step 1: Login with POS Manager credentials
print("Logging in as POS Manager...")
employee_page.enter_pos_manager_credentials()

# Step 2: Navigate to Employees section
print("Navigating to Employees section...")
employee_page.empl_stage.click()

# Step 3: Create a new employee
print("Creating new employee...")
employee_page.create_btn.click()

# Step 4: Fill in employee details
print("Entering employee name...")
employee_page.employees_name.send_keys("John Doe")

# Step 5: Save employee
print("Saving employee...")
employee_page.saved_message.click()

# Step 6: Verify employee created
print("Verifying employee creation...")
confirmation_text = employee_page.created_message.text
assert "Employee created" in confirmation_text, f"Expected 'Employee created', got '{confirmation_text}'"

print("Employee created successfully!")

# Cleanup
DriverManager.quit_driver()
```

### Employee Editing Workflow

```python
from pages.employee_page import EmployeePage
from utilities.driver_manager import DriverManager
import os

# Ensure credentials are set
os.environ['POS_MANAGER_USERNAME'] = 'posmanager50@info.com'
os.environ['POS_MANAGER_PASSWORD'] = 'posmanager'

driver = DriverManager.get_driver()
driver.get('https://testinium-demo.example.com')

employee_page = EmployeePage(driver)

# Login and navigate
employee_page.enter_pos_manager_credentials()
employee_page.empl_stage.click()

# Select existing employee
employee_page.choose_employee.click()

# Enter edit mode
employee_page.edit_employee.click()

# Update employee name
employee_page.name_edit.clear()
employee_page.name_edit.send_keys("Jane Smith (Updated)")

# Save changes
employee_page.saved_message.click()

print("Employee updated successfully!")

DriverManager.quit_driver()
```

### HR Navigation Example

```python
from pages.employee_page import EmployeePage
from utilities.driver_manager import DriverManager

driver = DriverManager.get_driver()
driver.get('https://testinium-demo.example.com')

employee_page = EmployeePage(driver)
employee_page.enter_pos_manager_credentials()

# Navigate through HR sections
print("Navigating to different HR sections...")

# Employees
employee_page.empl_stage.click()
print(f"Current URL: {driver.current_url}")

# Badges
employee_page.badges_btn.click()
print(f"Current URL: {driver.current_url}")

# Challenges
employee_page.challenges_btn.click()
print(f"Current URL: {driver.current_url}")

# Goals History
employee_page.goals_history_btn.click()
print(f"Current URL: {driver.current_url}")

# Departments
employee_page.departments_btn.click()
print(f"Current URL: {driver.current_url}")

DriverManager.quit_driver()
```

---

## Thread Safety

The `EmployeePage` class inherits thread-safe WebDriver management from `BasePage`. Each thread receives an independent WebDriver instance via `threading.local()` in `DriverManager`, ensuring safe parallel test execution.

**Parallel Execution Example:**

```python
import pytest
from pages.employee_page import EmployeePage
from utilities.driver_manager import DriverManager

@pytest.mark.parallel
def test_create_employee():
    """Can run in parallel - each thread has isolated WebDriver."""
    driver = DriverManager.get_driver()  # Thread-local instance
    driver.get('https://testinium-demo.example.com')
    
    employee_page = EmployeePage(driver)
    employee_page.enter_pos_manager_credentials()
    employee_page.empl_stage.click()
    employee_page.create_btn.click()
    employee_page.employees_name.send_keys("Test Employee")
    employee_page.saved_message.click()
    
    assert "Employee created" in employee_page.created_message.text
    
    DriverManager.quit_driver()

@pytest.mark.parallel
def test_navigate_badges():
    """Can run in parallel - isolated from test_create_employee."""
    driver = DriverManager.get_driver()  # Separate thread-local instance
    driver.get('https://testinium-demo.example.com')
    
    employee_page = EmployeePage(driver)
    employee_page.enter_pos_manager_credentials()
    employee_page.badges_btn.click()
    
    assert "badges" in driver.current_url.lower()
    
    DriverManager.quit_driver()
```

---

## Migration Notes

### From Java to Python

**Source File:** `src/main/java/com/testinium/pages/EmployeeP.java`  
**Target File:** `pages/employee_page.py`

**Pattern Transformations:**

| Java Pattern | Python Pattern | Rationale |
|--------------|----------------|-----------|
| `@FindBy` annotations | Private `_LOCATOR` tuples | Explicit locator definitions |
| Public `WebElement` fields | `@property` methods | Fresh element references prevent stale exceptions |
| `PageFactory.initElements()` | `wait_for_element()` in properties | Explicit waits ensure element readiness |
| Hardcoded credentials | Environment variables | Security remediation |
| Parameterized method bug | Removed broken method | Bug fix - parameters were ignored |

**Security Bug Fix:**

The Java implementation had a critical bug in the parameterized `enterPosManagerCredentials(String username, String password)` method which **completely ignored its parameters** and always used hardcoded credentials. This is fixed in Python by removing credential hardcoding entirely.

**Element Naming Consistency:**

| Java Name | Python Name | Notes |
|-----------|-------------|-------|
| `inputLogin` | `input_login` | snake_case per PEP 8 |
| `inputPass` | `input_password` | More descriptive name |
| `emplStage` | `empl_stage` | Preserved abbreviation |
| `badgesBtn` | `badges_btn` | Consistent button naming |
| `employeesName` | `employees_name` | Unchanged |

---

## Known Issues and Technical Debt

### Brittle Locators

**Issue:** Some element locators use brittle strategies that may fail if the application structure changes.

**Affected Elements:**

1. **`choose_employee`**: Uses absolute XPath `//html/body/div[1]/div[2]/div[2]/div/div/div/div[1]`
   - **Risk:** High - position-dependent
   - **Recommendation:** Update to class-based or data-attribute selector

2. **`edit_employee`**: Uses absolute XPath `//html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/button[1]`
   - **Risk:** High - position-dependent
   - **Recommendation:** Update to class-based or role-based selector

3. **`name_edit`**: Uses dynamically generated ID `o_field_input_678`
   - **Risk:** Medium - ID may change between sessions
   - **Recommendation:** Monitor stability; consider data-attribute selector if issues occur

**Recommended Improvements:**

```python
# Instead of absolute XPath
_CHOOSE_EMPLOYEE = (By.XPATH, "//html/body/div[1]/div[2]/div[2]/div/div/div/div[1]")

# Use more stable selector (requires application changes)
_CHOOSE_EMPLOYEE = (By.CSS_SELECTOR, "[data-testid='employee-card']")
# or
_CHOOSE_EMPLOYEE = (By.CLASS_NAME, "employee-list-item")
```

---

## Related Documentation

- [**BasePage API Reference**](base-page.md) - Base class with wait methods and element interaction utilities
- [**LoginPage API Reference**](login-page.md) - Standard user login (non-POS Manager)
- [**DriverManager API Reference**](../utilities/driver-manager.md) - WebDriver lifecycle management
- [**ConfigReader API Reference**](../utilities/config-reader.md) - Configuration access
- [**Employee Testing Guide**](../../guides/employee-testing.md) - User guide for employee management testing
- [**Configuration Management Guide**](../../guides/configuration-management.md) - Environment variable setup

---

## See Also

- **Behave Feature File:** `features/EmployeeFc.feature` - Employee management test scenarios
- **Step Definitions:** `features/steps/employee_steps.py` - Behave step implementations
- **Configuration:** `.env.example` - Environment variable template
- **Security Best Practices:** [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

**Last Updated:** Auto-generated from source code  
**Module Version:** 1.0.0  
**Python Version:** 3.9+  
**Selenium Version:** 4.15.2+

