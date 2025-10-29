# Common Error Messages

Quick reference guide to error messages encountered in the Testinium-QA Python test automation framework, with causes and solutions organized by category.

---

## Quick Reference Table

| Error Type | Error Message (Abbreviated) | Common Cause | Quick Solution | Details |
|------------|----------------------------|--------------|----------------|---------|
| **Import** | `ModuleNotFoundError` | Dependencies not installed | Activate venv, run `pip install -r requirements.txt` | [Import Errors](#1-modulenotfounderror--importerror) |
| **Import** | `ImportError: no known parent` | Missing `__init__.py` or wrong directory | Run from project root, check `__init__.py` files | [Import Errors](#1-modulenotfounderror--importerror) |
| **WebDriver** | `'chromedriver' executable needs to be in PATH` | WebDriver not found | `webdriver-manager` handles automatically | [WebDriver Errors](#2-webdriverexception-errors) |
| **WebDriver** | `SessionNotCreatedException` | Browser/driver version mismatch | Update browser or force driver update | [WebDriver Errors](#2-webdriverexception-errors) |
| **WebDriver** | `WebDriver not initialized` | Threading issue | Use `DriverManager.get_driver()` | [WebDriver Errors](#2-webdriverexception-errors) |
| **Selenium** | `StaleElementReferenceException` | Element DOM changed | Use property-based locators (automatic) | [Selenium Exceptions](#3-selenium-exceptions) |
| **Selenium** | `NoSuchElementException` | Element not found | Add explicit waits, verify locators | [Selenium Exceptions](#3-selenium-exceptions) |
| **Selenium** | `ElementNotInteractableException` | Element not ready | Use `wait_for_clickable()` | [Selenium Exceptions](#3-selenium-exceptions) |
| **Selenium** | `TimeoutException` | Element not found in time | Increase timeout, verify element exists | [Selenium Exceptions](#3-selenium-exceptions) |
| **Config** | `FileNotFoundError: config.yaml` | Config file missing | Verify `config/config.yaml` exists | [Configuration Errors](#4-configuration-errors) |
| **Config** | `yaml.YAMLError` | Invalid YAML syntax | Validate YAML syntax | [Configuration Errors](#4-configuration-errors) |
| **Config** | `KeyError` from config | Missing configuration key | Check config structure matches dataclasses | [Configuration Errors](#4-configuration-errors) |
| **Behave** | `Undefined step` | Step definition not found | Match step text exactly (case-sensitive) | [Behave Errors](#5-behave-errors) |
| **Behave** | Background step errors | Known Gherkin syntax issue | See workaround | [Behave Errors](#5-behave-errors) |
| **Behave** | Feature parsing errors | Invalid Gherkin syntax | Validate with `behave --dry-run` | [Behave Errors](#5-behave-errors) |
| **pytest** | Import errors | Package structure issue | Add `__init__.py` files | [pytest Errors](#6-pytest-errors) |
| **pytest** | Fixture errors | Scope or definition issue | Check fixture scope and definition | [pytest Errors](#6-pytest-errors) |
| **Headless** | Tests fail in CI | Headless not configured | Enable headless mode in config | [Headless Mode Errors](#7-headless-mode-errors) |
| **Parallel** | Driver shared between threads | Threading issue | Verify `threading.local()` pattern | [Parallel Execution Errors](#8-parallel-execution-errors) |
| **Reports** | Formatter not found | Reporter not installed | Install `allure-behave` or `behave-html-formatter` | [Report Generation Errors](#9-report-generation-errors) |
| **Reports** | Screenshot not captured | Hook not configured | Verify `environment.py` after_scenario hook | [Report Generation Errors](#9-report-generation-errors) |

---

## Detailed Error Explanations

### 1. ModuleNotFoundError / ImportError

#### Error: `ModuleNotFoundError: No module named 'selenium'`

**Full Error Message:**
```
ModuleNotFoundError: No module named 'selenium'
ModuleNotFoundError: No module named 'behave'
ModuleNotFoundError: No module named 'pytest'
```

**Cause:**
- Python dependencies are not installed
- Virtual environment is not activated
- Installation was done in different Python environment

**Solution:**

```bash
# Step 1: Ensure virtual environment is activated
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

# Step 2: Install all dependencies
pip install -r requirements.txt

# Step 3: Verify installation
pip list | grep selenium
pip list | grep behave

# Step 4: Test import
python -c "import selenium; print(selenium.__version__)"
```

**Source:** `README.md:606-613`

**See Also:**
- [Installation Issues Guide](installation-issues.md#dependency-installation-failures)
- [Getting Started: Installation](../getting-started/installation.md)

---

#### Error: `ImportError: attempted relative import with no known parent package`

**Full Error Message:**
```
ImportError: attempted relative import with no known parent package
ImportError: cannot import name 'DriverManager' from 'utilities'
```

**Cause:**
- Missing `__init__.py` files in package directories
- Running tests from wrong directory (not project root)
- `PYTHONPATH` not set correctly
- Package structure issues

**Solution:**

```bash
# Step 1: Verify __init__.py files exist in all packages
ls -la config/__init__.py
ls -la utilities/__init__.py
ls -la pages/__init__.py
ls -la features/steps/__init__.py

# Step 2: Run tests from project root directory
cd /path/to/testinium-qa-python
behave

# Step 3: If needed, set PYTHONPATH explicitly
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;%CD%          # Windows
```

**Verification:**
```python
# Test imports work correctly
python -c "from utilities.driver_manager import DriverManager; print('Success')"
python -c "from config.test_config import Config; print('Success')"
python -c "from pages.login_page import LoginPage; print('Success')"
```

**Source:** `README.md:633-640`

**See Also:**
- [Installation Issues Guide](installation-issues.md#import-errors)
- [Project Structure Documentation](../reference/project-structure.md)

---

### 2. WebDriverException Errors

#### Error: `WebDriverException: 'chromedriver' executable needs to be in PATH`

**Full Error Message:**
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH.
```

**Cause:**
- ChromeDriver binary not found in system PATH
- First-time execution before `webdriver-manager` downloads driver
- Network issues preventing driver download

**Solution:**

The framework uses `webdriver-manager` which handles ChromeDriver/GeckoDriver provisioning automatically. This error typically only appears if `webdriver-manager` is not installed:

```bash
# Ensure webdriver-manager is installed
pip install webdriver-manager

# No manual driver download needed!
# On first test execution, webdriver-manager will:
# 1. Detect your browser version
# 2. Download matching driver version
# 3. Cache it in ~/.wdm/drivers/
```

**Behind the Scenes** (in `utilities/driver_manager.py`):
```python
# Chrome driver setup
from webdriver_manager.chrome import ChromeDriverManager
chrome_service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Firefox driver setup (BUG FIX from Java version)
from webdriver_manager.firefox import GeckoDriverManager
firefox_service = FirefoxService(GeckoDriverManager().install())
driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
```

**Source:** `README.md:615-622`, `utilities/driver_manager.py:200-249`

**See Also:**
- [WebDriver Issues Guide](webdriver-issues.md#driver-binary-not-found)
- [API Reference: DriverManager](../api-reference/utilities/driver-manager.md)

---

#### Error: `SessionNotCreatedException: session not created`

**Full Error Message:**
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: 
This version of ChromeDriver only supports Chrome version 120
(Driver info: chromedriver=120.0.6099.71)
```

**Cause:**
- Browser version and driver version mismatch
- Browser was updated but driver cache is stale
- `webdriver-manager` unable to detect new browser version

**Solution:**

```bash
# Option 1: Update your browser to latest version
# Chrome: Help > About Google Chrome (auto-updates)
# Firefox: Help > About Firefox (auto-updates)

# Option 2: Force webdriver-manager to re-download driver
# Delete cache and re-run tests
rm -rf ~/.wdm/drivers/chromedriver/  # Linux/macOS
# Windows: Delete C:\Users\<username>\.wdm\drivers\chromedriver\

# Option 3: Update webdriver-manager package
pip install --upgrade webdriver-manager selenium

# Re-run tests - driver will be re-downloaded
behave
```

**Prevention:**
```yaml
# In CI/CD pipelines, always use latest browser versions
# GitHub Actions example:
- name: Setup Chrome
  uses: browser-actions/setup-chrome@latest
  
# Jenkins: Use Docker images with pre-installed browsers
FROM selenium/standalone-chrome:latest
```

**Source:** `README.md:642-649`

**See Also:**
- [WebDriver Issues Guide](webdriver-issues.md#browser-driver-version-mismatch)
- [Deployment: CI/CD Integration](../deployment/jenkins-integration.md)

---

#### Error: `WebDriver not initialized for thread`

**Full Error Message:**
```
AttributeError: 'thread._local' object has no attribute 'driver'
DriverInitializationError: WebDriver initialization failed for thread 'Thread-2'
```

**Cause:**
- Accessing WebDriver before calling `DriverManager.get_driver()`
- Thread-safety issue in parallel execution
- `threading.local()` storage not initialized for current thread

**Solution:**

**Always use `DriverManager.get_driver()`** to access WebDriver:

```python
# CORRECT - Thread-safe driver access
from utilities.driver_manager import DriverManager

def step_navigate_to_page(context):
    driver = DriverManager.get_driver()  # Gets thread-local instance
    driver.get("https://example.com")

# INCORRECT - Direct driver access (will fail)
def step_navigate_wrong(context):
    driver = context.driver  # May not exist yet
    driver.get("https://example.com")
```

**Understanding `threading.local()` Pattern:**

The framework uses `threading.local()` for thread isolation in parallel execution:

```python
# From utilities/driver_manager.py
class DriverManager:
    # Each thread gets its own driver instance
    _thread_local = threading.local()
    
    @classmethod
    def get_driver(cls) -> WebDriver:
        # Check if current thread has a driver
        if not hasattr(cls._thread_local, 'driver'):
            # Create new driver for this thread
            cls._thread_local.driver = cls._create_driver()
        return cls._thread_local.driver
```

**Key Points:**
- Each test thread gets its own isolated WebDriver instance
- No driver sharing between threads (prevents race conditions)
- Drivers are created lazily on first access per thread

**Source:** `utilities/driver_manager.py:82-196`

**See Also:**
- [Parallel Execution Issues Guide](parallel-execution-issues.md#thread-safety)
- [Architecture: Threading Pattern](../architecture/parallel-execution.md)
- [API Reference: DriverManager](../api-reference/utilities/driver-manager.md)

---

### 3. Selenium Exceptions

#### Error: `StaleElementReferenceException`

**Full Error Message:**
```
selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: 
element is not attached to the page document
```

**Cause:**
- Page DOM was updated after element was located
- Page navigation or partial refresh occurred
- AJAX/JavaScript modified the element
- Element was removed and re-added to DOM

**Solution (Automatic in This Framework):**

The framework uses **property-based locators** that automatically refresh elements on each access, preventing stale references:

```python
# FRAMEWORK PATTERN - Elements are re-located on each access
class LoginPage(BasePage):
    _INPUT_EMAIL = (By.NAME, "login")  # Locator tuple
    
    @property
    def input_email(self):
        # Element is located fresh every time this property is accessed
        return self.wait_for_element(self._INPUT_EMAIL)

# In step definitions
login_page = LoginPage(driver)
login_page.input_email.send_keys("user@example.com")  # Fresh element
login_page.input_email.clear()  # Fresh element again - no stale reference!
```

**Manual Solution (if needed):**

If you encounter stale elements outside page objects:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Re-locate element with explicit wait
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "myElement")))
element.click()

# Or use BasePage wait helpers
from pages.base_page import BasePage
page = BasePage(driver)
element = page.wait_for_element((By.ID, "myElement"))
```

**Source:** `README.md:651-662`, `pages/base_page.py:1-47`

**See Also:**
- [WebDriver Issues Guide](webdriver-issues.md#stale-element-reference)
- [Architecture: Property-Based Locators](../architecture/page-object-model.md)
- [Guide: Page Object Model](../guides/page-object-model.md)

---

#### Error: `NoSuchElementException`

**Full Error Message:**
```
selenium.common.exceptions.NoSuchElementException: Message: no such element: 
Unable to locate element: {"method":"css selector","selector":"#loginButton"}
```

**Cause:**
- Element does not exist on current page
- Incorrect locator (wrong ID, class, XPath, etc.)
- Element not yet loaded (timing issue)
- Element inside iframe or shadow DOM
- Element is dynamically generated

**Solution:**

**Step 1: Verify Element Exists**
```python
# Use browser DevTools to verify locator:
# 1. Open browser DevTools (F12)
# 2. Use Elements tab to inspect element
# 3. Test locator in Console:
$('#loginButton')  # jQuery-style ID selector
document.querySelector('#loginButton')  # Native JavaScript
```

**Step 2: Add Explicit Wait**
```python
# Use BasePage wait helpers (recommended)
from pages.base_page import BasePage

page = BasePage(driver)
element = page.wait_for_element((By.ID, "loginButton"), timeout=15)
element.click()

# Or use WebDriverWait directly
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 15)
element = wait.until(EC.presence_of_element_located((By.ID, "loginButton")))
```

**Step 3: Check for Common Issues**
```python
# Issue: Element in iframe
driver.switch_to.frame("iframeName")
element = driver.find_element(By.ID, "loginButton")

# Issue: Element requires scroll
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
actions.move_to_element(element).perform()

# Issue: Incorrect locator type
# Try different locator strategies:
element = driver.find_element(By.ID, "loginButton")  # ID
element = driver.find_element(By.NAME, "login")  # Name attribute
element = driver.find_element(By.CLASS_NAME, "btn-login")  # Class
element = driver.find_element(By.CSS_SELECTOR, ".btn.btn-login")  # CSS
element = driver.find_element(By.XPATH, "//button[@id='loginButton']")  # XPath
```

**Source:** `pages/base_page.py:129-165`

**See Also:**
- [WebDriver Issues Guide](webdriver-issues.md#element-not-found)
- [Guide: Wait Strategies](../guides/wait-strategies.md)
- [API Reference: BasePage](../api-reference/pages/base-page.md)

---

#### Error: `ElementNotInteractableException`

**Full Error Message:**
```
selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable
```

**Cause:**
- Element is not visible (hidden, zero size, opacity 0)
- Element is overlapped by another element
- Element is disabled
- Element is outside viewport
- Page is still loading/animating

**Solution:**

**Use `wait_for_clickable()` instead of `wait_for_element()`:**

```python
from pages.base_page import BasePage

page = BasePage(driver)

# WRONG - Element may exist but not be interactable
element = page.wait_for_element((By.ID, "submitButton"))
element.click()  # May throw ElementNotInteractableException

# CORRECT - Wait for element to be clickable
element = page.wait_for_clickable((By.ID, "submitButton"))
element.click()  # Safe to click
```

**Scroll Element Into View:**
```python
# If element is outside viewport
from selenium.webdriver.common.action_chains import ActionChains

element = driver.find_element(By.ID, "submitButton")
driver.execute_script("arguments[0].scrollIntoView(true);", element)
element.click()

# Or use ActionChains
actions = ActionChains(driver)
actions.move_to_element(element).perform()
actions.click(element).perform()
```

**Check Element State:**
```python
# Verify element is visible and enabled
element = driver.find_element(By.ID, "submitButton")
print(f"Displayed: {element.is_displayed()}")
print(f"Enabled: {element.is_enabled()}")
print(f"Size: {element.size}")
print(f"Location: {element.location}")
```

**Source:** `pages/base_page.py:147-165`

**See Also:**
- [Guide: Wait Strategies](../guides/wait-strategies.md#wait_for_clickable)
- [API Reference: BasePage.wait_for_clickable](../api-reference/pages/base-page.md#wait_for_clickable)

---

#### Error: `TimeoutException`

**Full Error Message:**
```
selenium.common.exceptions.TimeoutException: Message: 
Timeout waiting for element (By.ID, "dashboard") to be present
```

**Cause:**
- Element does not appear within configured timeout
- Element locator is incorrect
- Application is slow or unresponsive
- Network latency issues
- Element never appears due to application error

**Solution:**

**Step 1: Increase Timeout**
```python
# Override default timeout for specific wait
from pages.base_page import BasePage

page = BasePage(driver)
element = page.wait_for_element((By.ID, "dashboard"), timeout=30)  # 30 seconds

# Or adjust global timeout in config.yaml
# config/config.yaml:
timeouts:
  explicit: 20  # Increase from 10 to 20 seconds
  page_load: 60
```

**Step 2: Verify Element Actually Appears**
```python
# Check if element appears at all (manual test)
driver.get("https://example.com")
import time
time.sleep(30)  # Wait manually
element = driver.find_element(By.ID, "dashboard")  # Does it exist now?
```

**Step 3: Debug Wait Condition**
```python
# Add logging to understand what's happening
import logging
logging.basicConfig(level=logging.DEBUG)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.ID, "dashboard")))
    logger.debug(f"Element found: {element}")
except TimeoutException:
    logger.error("Element not found within timeout")
    logger.error(f"Current URL: {driver.current_url}")
    logger.error(f"Page title: {driver.title}")
    logger.error(f"Page source length: {len(driver.page_source)}")
    raise
```

**Step 4: Alternative Wait Strategies**
```python
# Try different wait conditions
from selenium.webdriver.support import expected_conditions as EC

# Option 1: Wait for visibility (not just presence)
element = wait.until(EC.visibility_of_element_located((By.ID, "dashboard")))

# Option 2: Wait for element to be clickable
element = wait.until(EC.element_to_be_clickable((By.ID, "dashboard")))

# Option 3: Wait for text in element
element = wait.until(EC.text_to_be_present_in_element((By.ID, "dashboard"), "Welcome"))
```

**Source:** `pages/base_page.py:129-228`

**See Also:**
- [Guide: Wait Strategies](../guides/wait-strategies.md)
- [Configuration Issues Guide](configuration-issues.md#timeout-configuration)
- [API Reference: Wait Helpers](../api-reference/utilities/wait-helpers.md)

---

### 4. Configuration Errors

#### Error: `FileNotFoundError: config.yaml`

**Full Error Message:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'config/config.yaml'
```

**Cause:**
- `config.yaml` file missing from `config/` directory
- Running tests from wrong directory
- Repository not fully cloned
- File accidentally deleted

**Solution:**

```bash
# Step 1: Verify file exists
ls -la config/config.yaml

# Step 2: If missing, ensure you're in project root
pwd  # Should show path ending in testinium-qa-python
cd /path/to/testinium-qa-python

# Step 3: Verify config directory structure
tree config/
# Expected:
# config/
# ├── __init__.py
# ├── config.yaml
# └── test_config.py

# Step 4: If file is truly missing, restore from repository
git checkout config/config.yaml
```

**Minimal `config.yaml` Structure:**
```yaml
browser:
  type: chrome
  headless: false
  window_size: [1920, 1080]

timeouts:
  explicit: 10
  page_load: 30
  element_presence: 10
  clickability: 10

application:
  base_url: ${BASE_URL:https://qa1.useblitzy.com}
  login_url: ${BASE_URL:https://qa1.useblitzy.com}/login

credentials:
  test_user:
    username: ${TEST_USER:user@example.com}
    password: ${TEST_PASSWORD:password123}

reporting:
  screenshots_on_failure: true
  screenshot_dir: reports/screenshots
  allure_results_dir: reports/allure-results
```

**See Also:**
- [Configuration Issues Guide](configuration-issues.md#missing-configuration-file)
- [Reference: Configuration Options](../reference/configuration-options.md)
- [Getting Started: Configuration](../getting-started/configuration.md)

---

#### Error: `yaml.YAMLError: mapping values are not allowed here`

**Full Error Message:**
```
yaml.scanner.ScannerError: mapping values are not allowed here
  in "config/config.yaml", line 15, column 12
```

**Cause:**
- Invalid YAML syntax (indentation, colons, quotes)
- Tabs used instead of spaces
- Missing colon after key
- Unquoted special characters
- Incorrect nesting

**Solution:**

**Step 1: Validate YAML Syntax**
```bash
# Use Python to validate YAML
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"

# Or use online validator: https://www.yamllint.com/
```

**Step 2: Common YAML Syntax Issues**

```yaml
# WRONG - Tab character used (not allowed in YAML)
browser:
	type: chrome  # Tab indent

# CORRECT - Use spaces (2 or 4 consistently)
browser:
  type: chrome  # 2-space indent

# WRONG - Missing colon
browser
  type: chrome

# CORRECT - Colon after key
browser:
  type: chrome

# WRONG - Unquoted URL with special characters
application:
  base_url: https://example.com?param=value&other=123

# CORRECT - Quote strings with special characters
application:
  base_url: "https://example.com?param=value&other=123"

# WRONG - Incorrect nesting
browser:
type: chrome
  headless: false

# CORRECT - Consistent indentation
browser:
  type: chrome
  headless: false
```

**Step 3: Fix and Retry**
```bash
# Edit config.yaml with proper indentation
nano config/config.yaml

# Validate again
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"

# Run tests
behave
```

**Source:** `config/test_config.py:1-24`

**See Also:**
- [Configuration Issues Guide](configuration-issues.md#yaml-syntax-errors)
- [Reference: Configuration File Format](../reference/configuration-options.md#yaml-syntax)

---

#### Error: `KeyError` from Configuration

**Full Error Message:**
```
KeyError: 'base_url'
KeyError: 'browser'
AttributeError: 'Config' object has no attribute 'application'
```

**Cause:**
- Configuration key missing from `config.yaml`
- Typo in configuration key name
- Configuration structure doesn't match dataclass structure
- Case sensitivity mismatch

**Solution:**

**Step 1: Verify Configuration Structure**

The configuration must match the dataclass structure in `config/test_config.py`:

```python
# Required structure (from config/test_config.py)
@dataclass
class Config:
    browser: BrowserConfig      # Required
    timeouts: TimeoutConfig     # Required
    application: ApplicationConfig  # Required
    credentials: CredentialsConfig  # Required
    reporting: ReportingConfig  # Required
```

**Step 2: Check `config.yaml` Has All Sections**

```yaml
# Minimal required structure
browser:
  type: chrome
  headless: false
  window_size: [1920, 1080]
  implicit_wait: 0

timeouts:
  explicit: 10
  page_load: 30
  element_presence: 10
  clickability: 10

application:
  base_url: "https://qa1.useblitzy.com"
  login_url: "https://qa1.useblitzy.com/login"
  web_table_url: "https://qa1.useblitzy.com/tables"
  empl_title: "Employee Management"

credentials:
  test_user:
    username: "user@example.com"
    password: "password123"

reporting:
  screenshots_on_failure: true
  screenshot_dir: "reports/screenshots"
  allure_results_dir: "reports/allure-results"
  output_dir: "reports"
```

**Step 3: Validate Configuration Loading**

```python
# Test configuration loads correctly
python -c "from config.test_config import get_config; c = get_config(); print(c)"

# Check specific values
python -c "from config.test_config import get_config; c = get_config(); print(c.application.base_url)"
```

**Step 4: Common KeyError Causes**

```python
# WRONG - Accessing non-existent key
config = get_config()
url = config.application.base_ur  # Typo: 'base_ur' instead of 'base_url'

# CORRECT - Use exact attribute names
url = config.application.base_url

# WRONG - Accessing missing section
url = config.api.endpoint  # No 'api' section in config

# CORRECT - Only access defined sections
url = config.application.base_url
```

**Source:** `config/test_config.py:78-130`

**See Also:**
- [Configuration Issues Guide](configuration-issues.md#missing-configuration-keys)
- [API Reference: Config Dataclasses](../api-reference/config/test-config.md)
- [Reference: Configuration Options](../reference/configuration-options.md)

---

### 5. Behave Errors

#### Error: `Undefined step definitions`

**Full Error Message:**
```
You can implement step definitions for undefined steps with these snippets:

@given(u'User is on the Testinium login page')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given User is on the Testinium login page')
```

**Cause:**
- Step definition not implemented in `features/steps/` directory
- Step text in `.feature` file doesn't match step definition exactly
- Case sensitivity mismatch
- Extra spaces or punctuation differences
- Step definition file not imported

**Solution:**

**Step 1: Check Exact Match (Case-Sensitive)**

```gherkin
# In Login.feature
Given User is on the upgenix login page
# Must match EXACTLY:

# In features/steps/login_steps.py
@given('User is on the upgenix login page')  # Exact match - works!

# WRONG examples:
@given('user is on the upgenix login page')  # Lowercase 'user' - NO MATCH
@given('User is on the Upgenix login page')  # Uppercase 'Upgenix' - NO MATCH
@given('User is on the upgenix login page.')  # Extra period - NO MATCH
```

**Step 2: Use `--dry-run` to Find Undefined Steps**

```bash
# Run Behave in dry-run mode to see all undefined steps
behave --dry-run

# Or with no-summary for cleaner output
behave --dry-run --no-summary

# Check specific feature file
behave features/Login.feature --dry-run
```

**Step 3: Verify Step Definition File Location**

```bash
# Step definitions must be in features/steps/ directory
tree features/steps/
# Expected:
# features/steps/
# ├── __init__.py          # Must exist!
# ├── login_steps.py
# ├── calendar_steps.py
# ├── contacts_steps.py
# └── ...

# Verify file has step decorators
grep -n "@given\|@when\|@then" features/steps/login_steps.py
```

**Step 4: Implement Missing Step**

```python
# Add to appropriate file in features/steps/
from behave import given, when, then

@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """Navigate to login page."""
    from pages.login_page import LoginPage
    from utilities.config_reader import ConfigReader
    
    driver = context.driver
    config = ConfigReader()
    login_url = config.get_property('application.login_url')
    driver.get(login_url)
```

**Source:** `README.md:624-631`, `features/steps/login_steps.py:90-124`

**See Also:**
- [Guide: Writing Step Definitions](../guides/step-definitions.md)
- [API Reference: Step Definitions](../api-reference/steps/login-steps.md)
- [Guide: Feature Files](../guides/feature-files.md)

---

#### Error: Background Step Errors (Known Issue)

**Full Error Message:**
```
Parser failure in state next_step, at line XX:
"Testinium CRM page is opened."
```

**Cause:**
- **KNOWN ISSUE**: 4 feature files have Gherkin syntax errors in Background sections
- Background contains prose text instead of Given/When/Then steps
- Affected files: `Calendar.feature`, `Inventory.feature`, `Notes.feature`, `Sales.feature`

**Background Syntax Problem:**

```gherkin
# WRONG - Prose in Background (current issue)
Feature: Calendar Management
  Background:
    Testinium CRM page is opened.  # Not a proper Given/When/Then step
    Login CRM.                     # Not a proper Given/When/Then step

  Scenario: Create Calendar Event
    Given User clicks calendar button
    ...

# CORRECT - Proper Gherkin syntax
Feature: Calendar Management
  Background:
    Given User is on the Testinium login page
    When User enters "salesmanager7@info.com" username
    And User enters "salesmanager" password
    And User clicks the login button
    Then User should see the CRM dashboard

  Scenario: Create Calendar Event
    Given User clicks calendar button
    ...
```

**Workaround:**

```bash
# Option 1: Run only feature files without Background issues
behave features/Login.feature
behave features/Contact.feature
behave features/EmployeeFc.feature
behave features/Logout.feature
behave features/Session.feature

# Option 2: Skip problematic features with tags
behave --tags=-@calendar --tags=-@inventory --tags=-@notes --tags=-@sales

# Option 3: Fix feature files (recommended)
# Edit Calendar.feature, Inventory.feature, Notes.feature, Sales.feature
# Replace prose with proper Given/When/Then steps
```

**Proper Fix (Edit Feature Files):**

```gherkin
# In Calendar.feature, Inventory.feature, Notes.feature, Sales.feature
# Replace Background section with:

Feature: Calendar Management
  Background: User logs in to CRM
    Given User is on the Testinium login page
    When User logs in with valid credentials
    Then User should see the CRM dashboard
```

**See Also:**
- [Guide: Feature Files - Background Syntax](../guides/feature-files.md#background-sections)
- [Reference: Gherkin Syntax](../reference/gherkin-syntax.md)

---

#### Error: Feature File Parsing Errors

**Full Error Message:**
```
ParserError: Parser failure in state next_step
ParserError: Expected one of: EOF, Scenario, Scenario Outline, Background, Tag, Feature
```

**Cause:**
- Invalid Gherkin syntax
- Missing keywords (Given, When, Then, And, But)
- Incorrect indentation
- Missing colons after keywords
- Mixing Scenarios and Scenario Outlines incorrectly

**Solution:**

**Step 1: Validate Feature File Syntax**

```bash
# Use --dry-run to catch syntax errors
behave --dry-run features/MyFeature.feature

# If error, Behave will show exact line number
```

**Step 2: Common Gherkin Syntax Rules**

```gherkin
# CORRECT Structure
Feature: Login Functionality
  As a user
  I want to log in
  So that I can access the application

  Background:
    Given User is on the login page

  Scenario: Valid login
    When User enters valid credentials
    And User clicks login button
    Then User should see dashboard

  Scenario Outline: Multiple users login
    When User enters "<username>" username
    And User enters "<password>" password
    And User clicks login button
    Then User should see dashboard

    Examples:
      | username | password |
      | user1    | pass1    |
      | user2    | pass2    |

# WRONG Examples:
# Missing colon
Feature Login Functionality

# Missing step keyword
User enters credentials  # Should be: When User enters credentials

# Incorrect indentation
Feature: Login
Scenario: Valid login  # Should be indented
  When User logs in

# Missing Examples table
Scenario Outline: Login
  When User enters "<username>"  # Needs Examples table below
```

**Step 3: Use Gherkin Linter (Optional)**

```bash
# Install gherkin linter
npm install -g gherkin-lint

# Lint feature files
gherkin-lint features/*.feature
```

**Source:** `features/Login.feature`, `features/steps/login_steps.py`

**See Also:**
- [Guide: Writing Feature Files](../guides/feature-files.md)
- [Reference: Gherkin Syntax](../reference/gherkin-syntax.md)
- [Behave Documentation](https://behave.readthedocs.io/)

---

### 6. pytest Errors

#### Error: Import Errors in pytest

**Full Error Message:**
```
ImportError: cannot import name 'TestConfig' from 'config'
ModuleNotFoundError: No module named 'utilities'
```

**Cause:**
- Missing `__init__.py` files in package directories
- Running pytest from wrong directory
- Package structure not recognized by pytest

**Solution:**

```bash
# Step 1: Verify __init__.py files exist
ls config/__init__.py
ls utilities/__init__.py
ls pages/__init__.py
ls tests/__init__.py

# Step 2: Create missing __init__.py files
touch config/__init__.py
touch utilities/__init__.py
touch pages/__init__.py
touch tests/__init__.py

# Step 3: Run pytest from project root
cd /path/to/testinium-qa-python
pytest

# Step 4: Verify PYTHONPATH if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

**pytest.ini Configuration:**

```ini
# pytest.ini
[pytest]
minversion = 7.0
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Ensure current directory in path
pythonpath = .
```

**Source:** `README.md:633-640`, `pytest.ini`

**See Also:**
- [Installation Issues Guide](installation-issues.md#package-structure-issues)
- [Reference: pytest Configuration](../reference/pytest-configuration.md)

---

#### Error: Fixture Errors

**Full Error Message:**
```
fixture 'driver' not found
ScopeMismatch: fixture 'config' has scope 'session', but the test requires scope 'function'
```

**Cause:**
- Fixture not defined or imported
- Fixture scope mismatch
- Fixture defined in wrong file

**Solution:**

**Define Fixtures in `conftest.py`:**

```python
# tests/conftest.py
import pytest
from utilities.driver_manager import DriverManager
from config.test_config import get_config

@pytest.fixture(scope="function")
def driver():
    """Provide WebDriver instance for test."""
    driver_instance = DriverManager.get_driver()
    yield driver_instance
    DriverManager.quit_driver()

@pytest.fixture(scope="session")
def config():
    """Provide configuration for test session."""
    return get_config()

@pytest.fixture(scope="function")
def login_page(driver):
    """Provide LoginPage instance."""
    from pages.login_page import LoginPage
    return LoginPage(driver)
```

**Use Fixtures in Tests:**

```python
# tests/test_login.py
def test_login_valid_credentials(driver, config, login_page):
    """Test login with valid credentials."""
    login_page.driver.get(config.application.login_url)
    login_page.login("user@example.com", "password123")
    assert "Dashboard" in driver.title
```

**Fixture Scope Options:**
- `function`: New instance per test function (default)
- `class`: New instance per test class
- `module`: New instance per test module
- `package`: New instance per test package
- `session`: One instance for entire test session

**See Also:**
- [Guide: Testing Guidelines](../contributing/testing-guidelines.md)
- [pytest Fixtures Documentation](https://docs.pytest.org/en/stable/fixture.html)

---

### 7. Headless Mode Errors

#### Error: Tests Pass Locally But Fail in CI

**Full Error Message:**
```
selenium.common.exceptions.WebDriverException: unknown error: Chrome failed to start
selenium.common.exceptions.WebDriverException: no DISPLAY environment variable
```

**Cause:**
- Headless mode not configured for CI environment
- Display server not available in CI
- Browser trying to open GUI in headless CI environment

**Solution:**

**Step 1: Enable Headless Mode in Configuration**

```yaml
# config/config.yaml
browser:
  type: chrome
  headless: true  # Enable for CI/CD
  window_size: [1920, 1080]
```

**Step 2: Override via Environment Variable**

```bash
# In CI pipeline (Jenkins, GitHub Actions, GitLab CI)
export HEADLESS=true
behave

# Or set in .env file for CI
echo "HEADLESS=true" >> .env
```

**Step 3: CI-Specific Configuration**

**GitHub Actions:**
```yaml
# .github/workflows/tests.yml
- name: Run tests in headless mode
  env:
    HEADLESS: true
  run: behave
```

**Jenkins:**
```groovy
// Jenkinsfile
environment {
    HEADLESS = 'true'
}
stages {
    stage('Test') {
        steps {
            sh 'behave'
        }
    }
}
```

**GitLab CI:**
```yaml
# .gitlab-ci.yml
test:
  variables:
    HEADLESS: "true"
  script:
    - behave
```

**Step 4: Linux Display Buffer (Alternative)**

```bash
# Install xvfb (virtual framebuffer) on Linux CI
sudo apt-get install xvfb

# Run tests with virtual display
xvfb-run behave

# Or start Xvfb manually
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
behave
```

**Source:** `README.md:664-675`, `utilities/driver_manager.py:250-310`

**See Also:**
- [Deployment: CI/CD Integration](../deployment/jenkins-integration.md)
- [Deployment: Docker](../deployment/docker.md)
- [Configuration: Browser Options](../reference/configuration-options.md#browser-settings)

---

#### Error: Screenshot Failures in Headless Mode

**Full Error Message:**
```
selenium.common.exceptions.WebDriverException: unknown error: session deleted because of page crash
IOError: cannot write mode RGBA as JPEG
```

**Cause:**
- Headless browser crash during screenshot capture
- Insufficient memory in CI environment
- Screenshot format incompatibility

**Solution:**

```bash
# Step 1: Increase memory allocation for headless browser
# In config/config.yaml or environment
export CHROME_ARGS="--disable-dev-shm-usage --no-sandbox"

# Step 2: Use PNG format for screenshots (not JPEG)
# In utilities/screenshot_helper.py, verify PNG format

# Step 3: Add error handling for screenshot capture
try:
    driver.save_screenshot(f"screenshot_{timestamp}.png")
except Exception as e:
    logger.warning(f"Screenshot capture failed: {e}")
```

**See Also:**
- [Troubleshooting: Report Generation Issues](report-generation-issues.md#screenshot-capture-failures)
- [Guide: Screenshot Management](../guides/screenshot-management.md)

---

### 8. Parallel Execution Errors

#### Error: Driver Shared Between Threads

**Full Error Message:**
```
selenium.common.exceptions.InvalidSessionIdException: invalid session id
RuntimeError: WebDriver instance is shared between threads
```

**Cause:**
- Multiple threads accessing same WebDriver instance
- Not using `threading.local()` pattern correctly
- Sharing driver instance between tests

**Solution:**

**Always Use `DriverManager.get_driver()`:**

```python
# CORRECT - Each thread gets its own driver
from utilities.driver_manager import DriverManager

def test_parallel_safe(context):
    driver = DriverManager.get_driver()  # Thread-local instance
    driver.get("https://example.com")
    # ... test logic ...
    DriverManager.quit_driver()  # Quit only this thread's driver

# WRONG - Sharing driver instance
shared_driver = webdriver.Chrome()  # Created once

def test_parallel_unsafe(context):
    shared_driver.get("https://example.com")  # RACE CONDITION!
```

**Understanding `threading.local()` Pattern:**

```python
# From utilities/driver_manager.py
class DriverManager:
    # Thread-local storage - each thread has independent storage
    _thread_local = threading.local()
    
    @classmethod
    def get_driver(cls):
        # Check if *current thread* has a driver
        if not hasattr(cls._thread_local, 'driver'):
            # Create driver for *this thread only*
            cls._thread_local.driver = cls._create_driver()
        return cls._thread_local.driver

# Thread 1: gets driver_1
# Thread 2: gets driver_2
# driver_1 != driver_2 (completely independent)
```

**Verify Parallel Execution:**

```bash
# Run tests in parallel with Behave
behave --processes 4 --parallel-element scenario

# Run tests in parallel with pytest
pytest -n 4  # 4 parallel workers
```

**Source:** `utilities/driver_manager.py:82-196`

**See Also:**
- [Parallel Execution Issues Guide](parallel-execution-issues.md)
- [Architecture: Threading Pattern](../architecture/parallel-execution.md)
- [Guide: Parallel Execution](../guides/parallel-execution.md)

---

#### Error: Race Conditions

**Full Error Message:**
```
AssertionError: Expected 'Dashboard' but got 'Login'
ElementNotInteractableException: element not interactable (race condition)
```

**Cause:**
- Shared mutable state between threads
- Global variables modified by multiple threads
- Test data conflicts
- Timing-dependent assertions

**Solution:**

**Avoid Shared Mutable State:**

```python
# WRONG - Shared global variable
test_counter = 0

def test_increment():
    global test_counter
    test_counter += 1  # RACE CONDITION!
    assert test_counter == 1  # May fail in parallel

# CORRECT - Thread-local state
import threading
thread_local = threading.local()

def test_increment():
    if not hasattr(thread_local, 'counter'):
        thread_local.counter = 0
    thread_local.counter += 1
    assert thread_local.counter == 1  # Safe
```

**Use Isolated Test Data:**

```python
# WRONG - Shared test user
def test_login():
    login("shared_user@example.com", "password")  # Conflicts!

# CORRECT - Unique test data per thread
import uuid

def test_login():
    unique_email = f"user_{uuid.uuid4()}@example.com"
    create_user(unique_email)
    login(unique_email, "password")
```

**See Also:**
- [Parallel Execution Issues Guide](parallel-execution-issues.md#race-conditions)
- [Guide: Parallel Execution Best Practices](../guides/parallel-execution.md#avoiding-race-conditions)

---

### 9. Report Generation Errors

#### Error: Formatter Not Found

**Full Error Message:**
```
behave.formatter._registry.FormatterNotFound: allure_behave.formatter:AllureFormatter
ModuleNotFoundError: No module named 'allure_behave'
```

**Cause:**
- Report formatter package not installed
- Typo in formatter name
- Incompatible package versions

**Solution:**

```bash
# Install Allure Behave formatter
pip install allure-behave

# Install Behave HTML formatter
pip install behave-html-formatter

# Install pytest HTML reporter
pip install pytest-html

# Verify installation
pip list | grep allure
pip list | grep behave

# Run with formatter
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results
```

**behave.ini Configuration:**

```ini
[behave]
format = allure_behave.formatter:AllureFormatter
       json
       html
outfiles = reports/allure-results
         reports/results.json
         reports/report.html
```

**See Also:**
- [Report Generation Issues Guide](report-generation-issues.md#formatter-installation)
- [Deployment: Report Publishing](../deployment/report-publishing.md)

---

#### Error: Screenshot Not Captured on Failure

**Full Error Message:**
```
# No error message - screenshots just don't appear in reports
```

**Cause:**
- `environment.py` after_scenario hook not configured correctly
- `SCREENSHOTS_ON_FAILURE` config set to `false`
- Screenshot directory not writable
- Hook not capturing exceptions properly

**Solution:**

**Step 1: Verify `environment.py` Hook**

```python
# features/environment.py
def after_scenario(context, scenario):
    """Capture screenshot on scenario failure."""
    if scenario.status == "failed":
        from utilities.screenshot_helper import capture_screenshot
        
        # Capture screenshot
        screenshot_path = capture_screenshot(
            driver=context.driver,
            scenario_name=scenario.name
        )
        
        # Attach to Allure report
        if screenshot_path:
            import allure
            allure.attach.file(
                screenshot_path,
                name=f"{scenario.name}_failure",
                attachment_type=allure.attachment_type.PNG
            )
```

**Step 2: Verify Configuration**

```yaml
# config/config.yaml
reporting:
  screenshots_on_failure: true  # Must be true
  screenshot_dir: "reports/screenshots"
```

**Step 3: Verify Directory Permissions**

```bash
# Create screenshot directory
mkdir -p reports/screenshots

# Verify writable
touch reports/screenshots/test.txt
rm reports/screenshots/test.txt

# Check permissions
ls -la reports/
```

**Step 4: Debug Screenshot Capture**

```python
# Add logging to after_scenario hook
import logging
logger = logging.getLogger(__name__)

def after_scenario(context, scenario):
    if scenario.status == "failed":
        logger.info(f"Scenario failed: {scenario.name}")
        try:
            screenshot_path = capture_screenshot(context.driver, scenario.name)
            logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Screenshot capture failed: {e}", exc_info=True)
```

**Source:** `README.md:677-684`, `features/environment.py`

**See Also:**
- [Report Generation Issues Guide](report-generation-issues.md#screenshot-capture)
- [Guide: Screenshot Management](../guides/screenshot-management.md)
- [API Reference: screenshot_helper](../api-reference/utilities/screenshot-helper.md)

---

#### Error: Allure Report Empty

**Full Error Message:**
```
# No error - Allure report generates but shows no tests
```

**Cause:**
- Allure formatter not configured correctly
- Results directory path incorrect
- Tests not run with Allure formatter enabled
- Allure results directory cleared before report generation

**Solution:**

**Step 1: Run Tests with Allure Formatter**

```bash
# Clean previous results
rm -rf reports/allure-results

# Run tests with Allure formatter
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results

# Verify results were created
ls -la reports/allure-results/
# Should see *.json files
```

**Step 2: Generate Allure Report**

```bash
# Install Allure CLI
# macOS: brew install allure
# Linux: Download from https://github.com/allure-framework/allure2/releases

# Generate HTML report
allure serve reports/allure-results

# Or generate static report
allure generate reports/allure-results -o reports/allure-report --clean
```

**Step 3: Verify behave.ini Configuration**

```ini
[behave]
format = allure_behave.formatter:AllureFormatter
outfiles = reports/allure-results

[behave.userdata]
allure_results_dir = reports/allure-results
```

**Source:** `behave.ini`, `README.md:196-252`

**See Also:**
- [Report Generation Issues Guide](report-generation-issues.md#allure-reports)
- [Deployment: Report Publishing](../deployment/report-publishing.md#allure-reports)
- [Allure Documentation](https://docs.qameta.io/allure/)

---

## Additional Resources

### Documentation Links

- **Troubleshooting Guides:**
  - [Installation Issues](installation-issues.md)
  - [WebDriver Issues](webdriver-issues.md)
  - [Configuration Issues](configuration-issues.md)
  - [Parallel Execution Issues](parallel-execution-issues.md)
  - [Report Generation Issues](report-generation-issues.md)

- **User Guides:**
  - [Getting Started](../getting-started/index.md)
  - [Configuration Management](../guides/configuration-management.md)
  - [Wait Strategies](../guides/wait-strategies.md)
  - [Parallel Execution](../guides/parallel-execution.md)

- **API Reference:**
  - [DriverManager](../api-reference/utilities/driver-manager.md)
  - [BasePage](../api-reference/pages/base-page.md)
  - [Config](../api-reference/config/test-config.md)

- **Architecture:**
  - [Threading Pattern](../architecture/parallel-execution.md)
  - [Page Object Model](../architecture/page-object-model.md)
  - [Wait Strategies](../architecture/wait-strategies.md)

### External Resources

- **Selenium Documentation:** https://www.selenium.dev/documentation/
- **Behave Documentation:** https://behave.readthedocs.io/
- **pytest Documentation:** https://docs.pytest.org/
- **Allure Framework:** https://docs.qameta.io/allure/
- **webdriver-manager:** https://github.com/SergeyPirogov/webdriver_manager

### Community Support

- **GitHub Issues:** Report bugs or request features
- **GitHub Discussions:** Ask questions and share knowledge
- **Stack Overflow:** Tag questions with `selenium`, `behave`, `python`

---

## Quick Diagnostic Checklist

When encountering an error, run through this checklist:

- [ ] **Virtual environment activated?**
  ```bash
  which python  # Should show venv/bin/python
  ```

- [ ] **Dependencies installed?**
  ```bash
  pip list | grep selenium
  pip list | grep behave
  ```

- [ ] **Running from project root?**
  ```bash
  pwd  # Should end in testinium-qa-python
  ls config/config.yaml  # Should exist
  ```

- [ ] **Configuration file valid?**
  ```bash
  python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
  ```

- [ ] **WebDriver initialized correctly?**
  ```python
  python -c "from utilities.driver_manager import DriverManager; d = DriverManager.get_driver(); print('OK'); DriverManager.quit_driver()"
  ```

- [ ] **Step definitions match feature file?**
  ```bash
  behave --dry-run
  ```

- [ ] **Logs available for debugging?**
  ```bash
  cat behave.log
  tail -n 50 reports/test.log
  ```

---

**Last Updated:** 2024
**Framework Version:** 1.0.0
**Python Version:** 3.9-3.12
**Selenium Version:** 4.15+
**Behave Version:** 1.2.6+

---

For more detailed troubleshooting, see the dedicated guides:
- [Installation Issues →](installation-issues.md)
- [WebDriver Issues →](webdriver-issues.md)
- [Configuration Issues →](configuration-issues.md)
- [Parallel Execution Issues →](parallel-execution-issues.md)
- [Report Generation Issues →](report-generation-issues.md)
