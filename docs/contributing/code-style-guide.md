# Code Style Guide

This guide defines the coding standards and conventions for the Testinium QA Python test automation framework. All contributors must follow these guidelines to ensure code consistency, maintainability, and quality across the project.

## Table of Contents

- [Python Version and Environment](#python-version-and-environment)
- [PEP 8 Compliance](#pep-8-compliance)
- [Code Formatting with Black](#code-formatting-with-black)
- [Import Sorting with isort](#import-sorting-with-isort)
- [Type Hints and mypy](#type-hints-and-mypy)
- [Naming Conventions](#naming-conventions)
- [Docstring Standards](#docstring-standards)
- [Code Organization](#code-organization)
- [Comments and Inline Documentation](#comments-and-inline-documentation)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Code Examples](#code-examples)

## Python Version and Environment

**Supported Python Versions:** 3.9, 3.10, 3.11, 3.12

**Target Version:** Python 3.9 (minimum compatibility baseline)

All code must be compatible with Python 3.9+ to ensure broad deployment compatibility. Use Python 3.9 syntax and standard library features as the baseline, with optional use of newer features when backward compatibility is maintained.

**Source:** `pyproject.toml:24` (python = "^3.9")

## PEP 8 Compliance

All Python code must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) - the official Python style guide.

### Line Length

**Maximum line length: 100 characters**

This is slightly more permissive than PEP 8's default 79 characters to accommodate modern wide-screen displays and reduce excessive line wrapping in test automation code.

```python
# ✅ GOOD: Line fits within 100 characters
def wait_for_element(self, locator, timeout=10, poll_frequency=0.5):
    return WebDriverWait(self.driver, timeout, poll_frequency).until(
        EC.presence_of_element_located(locator)
    )

# ❌ BAD: Line exceeds 100 characters
def wait_for_element_to_be_clickable_and_visible_with_custom_timeout_and_polling(self, locator, timeout, poll):
    return WebDriverWait(self.driver, timeout, poll).until(EC.element_to_be_clickable(locator))
```

**Source:** `pyproject.toml:94` (line-length = 100)

### Indentation

**Use 4 spaces per indentation level**

Never use tabs. Configure your editor to insert spaces when the Tab key is pressed.

```python
# ✅ GOOD: 4-space indentation
def login(self, username, password):
    self.input_email.send_keys(username)
    self.input_password.send_keys(password)
    self.login_button.click()

# ❌ BAD: 2-space or tab indentation
def login(self, username, password):
  self.input_email.send_keys(username)  # Only 2 spaces
	self.input_password.send_keys(password)  # Tab character
```

### Blank Lines

- **Two blank lines** before top-level class and function definitions
- **One blank line** between method definitions inside a class
- **One blank line** to separate logical sections within functions (sparingly)

```python
# ✅ GOOD: Proper blank line usage
import logging
from selenium.webdriver.common.by import By


logger = logging.getLogger(__name__)


class LoginPage:
    """Login page object."""

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        """Perform login with credentials."""
        self.input_email.send_keys(username)
        self.input_password.send_keys(password)
        self.login_button.click()
```

## Code Formatting with Black

The project uses [Black](https://black.readthedocs.io/) - "The Uncompromising Code Formatter" - to ensure 100% consistent code formatting.

### Black Configuration

```toml
[tool.black]
line-length = 100
target-version = ["py39", "py310", "py311", "py312"]
include = '\.pyi?$'
exclude = '''
/(
    \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
  | node_modules
  | venv
)/
'''
```

**Source:** `pyproject.toml:93-112`

### Running Black

**Format all Python files:**
```bash
black .
```

**Check formatting without modifications:**
```bash
black --check .
```

**Format specific file:**
```bash
black utilities/driver_manager.py
```

### Pre-Commit Integration

Configure Black to run automatically before each commit:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.9
```

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

### IDE Integration

**VS Code (.vscode/settings.json):**
```json
{
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "editor.formatOnSave": true
}
```

**PyCharm:**
1. Install Black: `pip install black`
2. Settings → Tools → External Tools → Add
3. Name: Black
4. Program: `$PyInterpreterDirectory$/black`
5. Arguments: `$FilePath$`
6. Working directory: `$ProjectFileDir$`

### Black Formatting Examples

```python
# Before Black formatting
def create_driver(browser_type,headless,window_size):
    if browser_type=="chrome":
        options=ChromeOptions()
        if headless:options.add_argument("--headless=new")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

# After Black formatting
def create_driver(browser_type, headless, window_size):
    if browser_type == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
```

**Key Black formatting rules:**
- Spaces around operators (`=`, `==`, `+`, etc.)
- Trailing commas in multi-line structures
- Consistent quote usage (prefers double quotes)
- Automatic line wrapping at 100 characters
- Consistent parentheses and bracket spacing

## Import Sorting with isort

The project uses [isort](https://pycqa.github.io/isort/) to automatically sort and organize import statements.

### isort Configuration

```toml
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
skip_glob = [
    "venv/*",
    ".venv/*",
    "build/*",
    "dist/*",
    "*.egg-info/*",
]
```

**Source:** `pyproject.toml:142-156`

### Import Organization

Imports must be organized into three groups, separated by blank lines:

1. **Standard library imports**
2. **Third-party package imports**
3. **Local application imports**

Within each group, imports are sorted alphabetically.

```python
# ✅ GOOD: Properly organized imports
# Standard library imports
import logging
import threading
from typing import Optional

# Third-party package imports
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Local application imports
from config.test_config import Config, get_config
from pages.base_page import BasePage
from pages.login_page import LoginPage
from utilities.config_reader import ConfigReader
from utilities.driver_manager import DriverManager
```

### Running isort

**Sort imports in all files:**
```bash
isort .
```

**Check import sorting without modifications:**
```bash
isort --check-only .
```

**Sort specific file:**
```bash
isort utilities/driver_manager.py
```

### isort with Black Compatibility

The `profile = "black"` configuration ensures isort's formatting is 100% compatible with Black, preventing conflicts between the two tools.

```python
# isort + Black compatible multi-line imports
from selenium.webdriver.support import (
    expected_conditions as EC,
    select,
    wait,
)
```

## Type Hints and mypy

The project uses Python type hints and [mypy](http://mypy-lang.org/) for static type checking to catch bugs early and improve code documentation.

### mypy Configuration

```toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
ignore_missing_imports = true
```

**Source:** `pyproject.toml:114-131`

### Type Hint Requirements

**All function signatures must include type hints:**

```python
# ✅ GOOD: Complete type hints
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

def get_driver(cls) -> WebDriver:
    """Get WebDriver instance."""
    pass

def wait_for_element(
    self,
    locator: tuple[str, str],
    timeout: int = 10,
    poll_frequency: float = 0.5
) -> WebElement:
    """Wait for element with timeout."""
    pass

def get_property(self, key: str, default: Optional[str] = None) -> Optional[str]:
    """Get configuration property."""
    pass

# ❌ BAD: Missing type hints
def get_driver(cls):
    """Get WebDriver instance."""
    pass

def wait_for_element(self, locator, timeout=10, poll_frequency=0.5):
    """Wait for element with timeout."""
    pass
```

### Common Type Annotations

```python
from typing import Optional, Union, List, Dict, Tuple, Any

# Basic types
name: str = "test"
count: int = 42
is_valid: bool = True
timeout: float = 10.5

# Optional types (can be None)
result: Optional[str] = None
driver: Optional[WebDriver] = None

# Collections
usernames: List[str] = ["user1", "user2"]
config: Dict[str, Any] = {"timeout": 10, "headless": True}
locator: Tuple[str, str] = (By.ID, "username")

# Union types (multiple possible types)
timeout: Union[int, float] = 10
value: Union[str, int, bool] = "test"

# Return type for functions that don't return a value
def cleanup() -> None:
    """Cleanup resources."""
    pass
```

### Running mypy

**Type check all files:**
```bash
mypy .
```

**Type check specific file:**
```bash
mypy utilities/driver_manager.py
```

**Type check with verbose output:**
```bash
mypy --verbose utilities/driver_manager.py
```

### mypy Overrides for Third-Party Libraries

Some third-party libraries lack type stubs. Configure mypy to ignore missing imports:

```toml
[[tool.mypy.overrides]]
module = [
    "selenium.*",
    "behave.*",
    "allure.*",
    "faker.*",
]
ignore_missing_imports = true
```

**Source:** `pyproject.toml:133-140`

## Naming Conventions

Consistent naming conventions improve code readability and maintainability.

### General Naming Rules

| Code Element | Convention | Examples |
|--------------|-----------|----------|
| **Modules** | `snake_case` | `driver_manager.py`, `config_reader.py`, `login_steps.py` |
| **Packages** | `snake_case` | `utilities`, `pages`, `config`, `features` |
| **Classes** | `PascalCase` | `DriverManager`, `LoginPage`, `BasePage`, `ConfigReader` |
| **Exceptions** | `PascalCase` ending with `Error` | `DriverInitializationError`, `ConfigurationError` |
| **Functions** | `snake_case` | `get_driver()`, `wait_for_element()`, `capture_screenshot()` |
| **Methods** | `snake_case` | `login()`, `click_element()`, `get_element_text()` |
| **Variables** | `snake_case` | `driver`, `config`, `timeout`, `user_name` |
| **Constants** | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT`, `BROWSER_TYPE`, `MAX_RETRIES` |
| **Private members** | `_leading_underscore` | `_thread_local`, `_create_driver()`, `_INPUT_EMAIL` |
| **Protected members** | `_leading_underscore` | `_driver`, `_config`, `_wait` |
| **Test functions** | `test_` prefix | `test_get_driver_chrome()`, `test_login_valid_credentials()` |
| **Step definitions** | `step_` prefix | `step_navigate_to_login_page()`, `step_enter_username()` |

### Naming Examples

**Modules and Packages:**
```python
# ✅ GOOD
utilities/driver_manager.py
utilities/config_reader.py
utilities/wait_helpers.py
pages/login_page.py
features/steps/login_steps.py

# ❌ BAD
utilities/DriverManager.py  # Should be snake_case
utilities/configReader.py   # Should be snake_case
pages/LoginPage.py          # Should be snake_case
```

**Classes:**
```python
# ✅ GOOD
class DriverManager:
    pass

class LoginPage(BasePage):
    pass

class DriverInitializationError(Exception):
    pass

# ❌ BAD
class driver_manager:  # Should be PascalCase
    pass

class loginPage:  # Should be PascalCase
    pass

class DriverError:  # Should end with Error for exceptions
    pass
```

**Functions and Methods:**
```python
# ✅ GOOD
def get_driver() -> WebDriver:
    pass

def wait_for_element(locator, timeout):
    pass

def capture_screenshot(filename):
    pass

# ❌ BAD
def GetDriver():  # Should be snake_case
    pass

def waitForElement(locator, timeout):  # Should be snake_case (no camelCase)
    pass

def CaptureScreenshot(filename):  # Should be snake_case
    pass
```

**Variables and Constants:**
```python
# ✅ GOOD
driver = DriverManager.get_driver()
config_reader = ConfigReader()
user_name = "testuser"
DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3
BROWSER_TYPE = "chrome"

# ❌ BAD
Driver = DriverManager.get_driver()  # Variables should be snake_case
ConfigReader = ConfigReader()  # Don't use class names for variables
userName = "testuser"  # Should be snake_case (no camelCase)
default_timeout = 10  # Constants should be UPPER_SNAKE_CASE
```

**Private and Protected Members:**
```python
# ✅ GOOD
class DriverManager:
    _thread_local = threading.local()  # Class-level private attribute
    
    @classmethod
    def _create_driver(cls) -> WebDriver:  # Private method
        pass

class LoginPage(BasePage):
    _INPUT_EMAIL = (By.NAME, "login")  # Private locator constant
    _INPUT_PASSWORD = (By.NAME, "password")
    
    def __init__(self, driver):
        self._driver = driver  # Protected instance attribute

# ❌ BAD
class DriverManager:
    thread_local = threading.local()  # Should be private (_thread_local)
    
    def create_driver(cls):  # Should be private if internal (_create_driver)
        pass
```

**Test Functions:**
```python
# ✅ GOOD
def test_get_driver_chrome_default():
    """Test driver creation with default Chrome configuration."""
    pass

def test_login_valid_credentials():
    """Test login with valid username and password."""
    pass

# ❌ BAD
def get_driver_test():  # Must start with test_
    pass

def testLoginValidCredentials():  # Should be snake_case
    pass
```

**Behave Step Definitions:**
```python
# ✅ GOOD
@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """Navigate to login page."""
    pass

@when('User enters "{username}" username')
def step_enter_username(context, username):
    """Enter username into login form."""
    pass

# ❌ BAD
@given('User is on the upgenix login page')
def navigate_to_login_page(context):  # Should have step_ prefix
    pass

@when('User enters "{username}" username')
def stepEnterUsername(context, username):  # Should be snake_case
    pass
```

## Docstring Standards

All modules, classes, and public functions must have comprehensive docstrings following **Google-style Python docstrings**.

### Google-Style Docstring Format

```python
def function_name(arg1, arg2, arg3=None):
    """Short one-line summary of function purpose.

    Longer description providing additional context, implementation details,
    design decisions, and usage guidance. Can span multiple paragraphs.

    Args:
        arg1 (str): Description of first argument
        arg2 (int): Description of second argument
        arg3 (Optional[bool]): Description of optional third argument.
            Defaults to None.

    Returns:
        dict: Description of return value, including structure if complex

    Raises:
        ValueError: When and why this exception is raised
        TypeError: When and why this exception is raised

    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        {'status': 'success', 'count': 42}

    Note:
        Any additional notes, warnings, or important information
    """
    pass
```

### Module Docstrings

Every Python module must start with a comprehensive module docstring.

**Required Sections:**
1. Module name/title
2. Purpose and responsibilities
3. Migration context (if applicable from Java)
4. Key features or critical changes
5. Example usage
6. Dependencies (if complex)

**Example from utilities/driver_manager.py:**

```python
"""
Driver Manager Module

Thread-safe WebDriver lifecycle management for parallel test execution.

This module replaces Java's Driver.java with Python implementation:
- Threading.local() replaces InheritableThreadLocal for thread safety
- webdriver-manager handles automatic driver binary provisioning
- Explicit waits ONLY (eliminates 10-second implicit wait anti-pattern)
- Configuration-driven browser selection (Chrome, Firefox)
- Lazy initialization with proper cleanup

CRITICAL BUG FIX:
    Original Java Driver.java line 37 incorrectly called:
        WebDriverManager.chromedriver().setup()
    for Firefox browser, causing Firefox tests to fail.

    This Python implementation correctly uses:
        GeckoDriverManager().install()
    for Firefox, ensuring proper GeckoDriver binary provisioning.

ARCHITECTURAL CHANGES FROM JAVA VERSION:
    1. NO implicit waits (Java had 10s on lines 34, 40) - explicit waits only
    2. threading.local() provides thread-level isolation (not child inheritance)
    3. webdriver-manager caches binaries in ~/.wdm/drivers/
    4. Comprehensive logging replaces System.out.println
    5. Proper exception handling replaces silent failures
    6. Selenium 4.x syntax (headless=new, ChromeService, FirefoxService)

Example Usage:
    >>> from utilities.driver_manager import DriverManager
    >>> # Get WebDriver instance for current thread
    >>> driver = DriverManager.get_driver()
    >>> driver.get("https://example.com")
    >>> # Cleanup after test
    >>> DriverManager.quit_driver()
"""
```

**Source:** `utilities/driver_manager.py:1-37`

### Class Docstrings

Every class must have a comprehensive docstring explaining its purpose, attributes, and usage.

**Required Sections:**
1. Class purpose and responsibilities
2. Attributes (if not obvious)
3. Thread safety notes (if applicable)
4. Example usage

**Example from utilities/driver_manager.py:**

```python
class DriverManager:
    """
    Thread-safe WebDriver lifecycle manager using threading.local().

    Provides centralized WebDriver instantiation, configuration, and cleanup
    with strict thread isolation for parallel test execution. Replaces Java's
    InheritableThreadLocal pattern with Python threading.local().

    Thread Safety:
        - Each thread gets its own WebDriver instance via threading.local()
        - No shared state between threads (prevents race conditions)
        - Compatible with behave-parallel (process-based parallelism)
        - Compatible with pytest-xdist (thread/process parallelism)

    Supported Browsers:
        - Chrome (default): ChromeDriverManager with Selenium 4.x
        - Firefox: GeckoDriverManager with Selenium 4.x (BUG FIXED)

    Configuration:
        Reads from config/config.yaml via ConfigReader:
        - browser.type: 'chrome' or 'firefox' (default: 'chrome')
        - browser.headless: true/false (default: false)
        - browser.window_size: [width, height] (optional)

    Example:
        >>> # Get driver for current thread
        >>> driver = DriverManager.get_driver()
        >>> driver.get("https://example.com")
        >>>
        >>> # Each thread gets its own driver
        >>> # Thread 1: driver_1 = DriverManager.get_driver()
        >>> # Thread 2: driver_2 = DriverManager.get_driver()
        >>> # driver_1 != driver_2 (different instances)
        >>>
        >>> # Cleanup
        >>> DriverManager.quit_driver()
    """
```

**Source:** `utilities/driver_manager.py:82-125`

### Exception Class Docstrings

Custom exception classes must document when they are raised and how to handle them.

**Example from utilities/driver_manager.py:**

```python
class DriverInitializationError(Exception):
    """
    Custom exception for WebDriver initialization failures.

    Raised when:
    - Unsupported browser type specified in configuration
    - WebDriver binary download fails
    - Browser process fails to start
    - Driver service initialization fails
    - Configuration missing or invalid

    This provides explicit error handling replacing Java's silent failures
    and generic exceptions.

    Example:
        >>> try:
        ...     driver = DriverManager.get_driver()
        ... except DriverInitializationError as e:
        ...     logger.error(f"Failed to initialize driver: {e}")
        ...     raise
    """
```

**Source:** `utilities/driver_manager.py:59-79`

### Method Docstrings

Every public method must have a comprehensive docstring with Args, Returns, Raises, and Example sections.

**Required Sections:**
1. Short one-line summary
2. Longer description (if needed)
3. Args: All parameters with types and descriptions
4. Returns: Return type and description
5. Raises: All exceptions that can be raised
6. Example: Usage example with expected output
7. Java equivalent: If migrated from Java (cite original file and line)

**Example from utilities/driver_manager.py:**

```python
@classmethod
def get_driver(cls) -> WebDriver:
    """
    Get WebDriver instance for current thread with lazy initialization.

    Returns same driver instance for repeated calls within same thread.
    Creates new driver on first call per thread using _create_driver().

    This replaces Java's getDriver() method with equivalent functionality:
    - Lazy initialization (create only when needed)
    - Thread-local storage (one driver per thread)
    - Configuration-driven browser selection

    Thread Safety:
        Each thread calling this method gets its own WebDriver instance
        stored in threading.local(). No synchronization needed since
        threading.local() provides thread-isolated storage.

    Returns:
        WebDriver: Thread-local WebDriver instance (Chrome or Firefox)

    Raises:
        DriverInitializationError: If driver creation fails
        ValueError: If unsupported browser type configured
        ConfigurationError: If required configuration missing

    Example:
        >>> driver = DriverManager.get_driver()
        >>> driver.get("https://example.com")
        >>> # Subsequent calls return same instance
        >>> same_driver = DriverManager.get_driver()
        >>> assert driver is same_driver
    """
```

**Source:** `utilities/driver_manager.py:132-163`

### Behave Step Definition Docstrings

Step definitions must document the Gherkin step they implement, parameters, and Java equivalent (if migrated).

**Example from features/steps/login_steps.py:**

```python
@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """
    Navigate to login page using configured URL from config.yaml.

    This step implements the Background step from Login.feature, executed before
    each scenario to ensure user starts on the login page. Replaces Java
    implementation from LoginSD.java lines 19-24.

    Java equivalent:
        @Given("User is on the upgenix login page")
        public void user_is_on_the_upgenix_login_page() {
            String url = ConfigurationReader.getProperty("web.table.url");
            Driver.getDriver().get(url);
        }

    Configuration:
        Retrieves login URL from config.yaml via ConfigReader.get_property('web.table.url').
        Falls back to BASE_URL environment variable if key not found in YAML.

    Args:
        context: Behave context object containing driver and configuration
                context.driver: WebDriver instance for browser navigation

    Raises:
        KeyError: If 'web.table.url' configuration key missing and no default provided
        WebDriverException: If navigation to URL fails

    Example:
        Given User is on the upgenix login page
        # Browser navigates to https://testinium.example.com/login
    """
```

**Source:** `features/steps/login_steps.py:90-120`

### Package __init__.py Docstrings

Package initialization files must document the package purpose and what it exports.

**Example from tests/__init__.py:**

```python
"""
Test Suite for Testinium QA Python Test Automation Framework.

This package contains pytest-based unit tests for the test automation framework
itself, validating utilities, configuration, and driver management components.

Purpose:
    - Validate framework reliability through automated testing
    - Ensure driver manager thread safety and singleton pattern correctness
    - Verify configuration reader handles YAML, environment variables, and errors
    - Test critical bug fixes from Java-to-Python migration (Firefox driver setup)
    - Enable pytest discovery of test modules (test_*.py)
    - Support continuous integration and quality assurance

Test Modules:
    - test_driver_manager.py: Unit tests for WebDriver lifecycle management,
      thread-local isolation, and browser driver initialization
    - test_config.py: Unit tests for YAML configuration parsing, environment
      variable overrides, and error handling

Test Execution:
    Run all tests:
        $ pytest tests/ -v
    
    Run specific test module:
        $ pytest tests/test_driver_manager.py -v
    
    Run with coverage:
        $ pytest tests/ --cov=utilities --cov-report=html

Standards:
    - All test functions must start with 'test_' for pytest discovery
    - Use pytest fixtures for setup and teardown
    - Use unittest.mock for isolating external dependencies
    - Validate proper exception handling (no swallowed errors)
    - Test thread safety for parallel execution scenarios
"""
```

**Source:** `tests/__init__.py:1-53`

## Code Organization

Organize code logically to improve maintainability and navigation.

### File Organization Principles

1. **One class per file** for page objects (LoginPage → login_page.py)
2. **Related utilities grouped** in same module (wait_helpers.py contains all wait utilities)
3. **Feature-specific step definitions** in dedicated files (login_steps.py for Login.feature)
4. **Logical import order** (standard library, third-party, local)

### Module Structure

**Standard module structure:**

```python
"""
Module Docstring
Comprehensive description of module purpose, features, and usage
"""

# Standard library imports
import logging
import threading
from typing import Optional

# Third-party package imports
from selenium import webdriver
from selenium.webdriver.common.by import By

# Local application imports
from config.test_config import Config
from utilities.config_reader import ConfigReader

# Module-level constants
DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3
BROWSER_TYPE = "chrome"

# Configure module logger
logger = logging.getLogger(__name__)


class MyClass:
    """Class implementation"""
    pass


def my_function():
    """Function implementation"""
    pass
```

### Class Organization

**Standard class structure:**

```python
class LoginPage(BasePage):
    """Login page object."""
    
    # Class-level constants (locators, configuration)
    _INPUT_EMAIL = (By.NAME, "login")
    _INPUT_PASSWORD = (By.NAME, "password")
    _LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    def __init__(self, driver):
        """Initialize with WebDriver instance."""
        super().__init__(driver)
    
    # Properties (element accessors)
    @property
    def input_email(self):
        """Email input field."""
        return self.wait_for_element(self._INPUT_EMAIL)
    
    @property
    def input_password(self):
        """Password input field."""
        return self.wait_for_element(self._INPUT_PASSWORD)
    
    # Public methods (business logic)
    def login(self, username, password):
        """Perform login with credentials."""
        self.input_email.send_keys(username)
        self.input_password.send_keys(password)
        self.login_button.click()
    
    # Private methods (internal helpers)
    def _validate_login_state(self):
        """Internal method to validate login state."""
        pass
```

### Feature Step Definition Organization

Group step definitions by step type (Given, When, Then) with clear section comments:

```python
# ============================================================================
# GIVEN STEPS - Preconditions and Setup
# ============================================================================

@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """Navigate to login page."""
    pass


# ============================================================================
# WHEN STEPS - Actions
# ============================================================================

@when('User enters "{username}" username')
def step_enter_username(context, username):
    """Enter username into login form."""
    pass


# ============================================================================
# THEN STEPS - Assertions and Verifications
# ============================================================================

@then('User should see the dashboard')
def step_verify_dashboard_displayed(context):
    """Verify user successfully logged in to dashboard."""
    pass
```

## Comments and Inline Documentation

Use comments to explain **why**, not **what**. The code itself should be clear enough to explain what it does.

### Good Comments

```python
# ✅ GOOD: Explains WHY and references critical context

# threading.local() provides thread-level storage for WebDriver instances
# Each thread calling get_driver() receives its own isolated WebDriver
# This prevents race conditions in parallel test execution
_thread_local = threading.local()

# CRITICAL BUG FIX: Original Java implementation (Driver.java:37) incorrectly
# called ChromeDriverManager for Firefox browser, causing test failures.
# This Python implementation correctly uses GeckoDriverManager for Firefox.
if browser_type == "firefox":
    service = FirefoxService(GeckoDriverManager().install())
```

**Source:** `utilities/driver_manager.py:127-129` and similar patterns

### Bad Comments

```python
# ❌ BAD: States the obvious, adds no value

# Get the driver
driver = DriverManager.get_driver()

# Set the username
username_field.send_keys(username)

# Click login button
login_button.click()

# Check if element is displayed
if element.is_displayed():
    pass
```

### Migration Notes

When migrating from Java, document the original Java equivalent and note critical changes:

```python
# Replaces Java Driver.java getDriver() method (lines 32-43)
# Key change: NO implicit wait (Java had 10s implicit wait on line 34)
# This Python implementation uses ONLY explicit waits via BasePage
def get_driver(cls) -> WebDriver:
    """Get WebDriver instance for current thread."""
    pass
```

### Thread Safety Documentation

Always document thread-safety guarantees and mechanisms:

```python
class DriverManager:
    """
    Thread-safe WebDriver lifecycle manager.
    
    Thread Safety:
        - Each thread gets its own WebDriver instance via threading.local()
        - No shared state between threads (prevents race conditions)
        - Compatible with behave-parallel (process-based parallelism)
    """
    
    # threading.local() provides thread-isolation for WebDriver instances
    # No locks needed - each thread has independent storage
    _thread_local = threading.local()
```

### Configuration and Design Decision Documentation

Document configuration precedence and design decisions:

```python
# Configuration precedence (highest to lowest):
# 1. Environment variables (.env file)
# 2. config.yaml values
# 3. Default values in code
config_value = os.getenv('TIMEOUT') or yaml_config.get('timeout') or DEFAULT_TIMEOUT
```

### Bug Fix Documentation

Always reference the original bug and how it was fixed:

```python
# BUG FIX: Original Java code swallowed IOException with printStackTrace (line 45)
# This Python implementation properly propagates exceptions for visibility
try:
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError as e:
    logger.error(f"Configuration file not found: {config_file}")
    raise ConfigurationError(f"Missing configuration file: {config_file}") from e
```

## Anti-Patterns to Avoid

Avoid these common anti-patterns that reduce code quality and cause issues.

### 1. Implicit Waits

**❌ NEVER use implicit waits:**

```python
# ❌ BAD: Implicit waits cause issues with explicit waits
driver.implicitly_wait(10)  # NEVER DO THIS
```

**✅ ALWAYS use explicit waits:**

```python
# ✅ GOOD: Explicit waits only
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "username"))
)
```

**Rationale:** Implicit waits conflict with explicit waits and cause unpredictable timing issues. The framework uses ONLY explicit waits as specified in Agent Action Plan Section 0.4.3.

### 2. Hardcoded Credentials

**❌ NEVER hardcode credentials:**

```python
# ❌ BAD: Hardcoded credentials (security vulnerability)
username = "admin@example.com"
password = "P@ssw0rd123"
```

**✅ ALWAYS use environment variables or configuration:**

```python
# ✅ GOOD: Credentials from environment variables
import os
username = os.getenv('TEST_USERNAME')
password = os.getenv('TEST_PASSWORD')

# ✅ GOOD: Credentials from configuration
config = ConfigReader()
username = config.get_property('credentials.username')
password = config.get_property('credentials.password')
```

### 3. Swallowed Exceptions

**❌ NEVER swallow exceptions silently:**

```python
# ❌ BAD: Exception swallowed without logging or re-raising
try:
    driver = create_driver()
except Exception:
    pass  # Silent failure - debugging nightmare

# ❌ BAD: Exception logged but not propagated
try:
    config = load_config()
except FileNotFoundError as e:
    print(f"Error: {e}")  # Logged but execution continues incorrectly
```

**✅ ALWAYS log and re-raise or handle appropriately:**

```python
# ✅ GOOD: Exception logged and re-raised with context
try:
    driver = create_driver()
except WebDriverException as e:
    logger.exception("Failed to create WebDriver instance")
    raise DriverInitializationError(f"WebDriver creation failed: {e}") from e

# ✅ GOOD: Exception handled with fallback
try:
    config = load_yaml_config()
except FileNotFoundError:
    logger.warning("YAML config not found, using defaults")
    config = get_default_config()
```

### 4. Thread.sleep() or time.sleep()

**❌ NEVER use hardcoded sleep statements:**

```python
# ❌ BAD: Hardcoded sleep (unreliable, wastes time)
import time
driver.find_element(By.ID, "username").send_keys("test")
time.sleep(3)  # NEVER DO THIS
driver.find_element(By.ID, "login").click()
```

**✅ ALWAYS use explicit waits:**

```python
# ✅ GOOD: Explicit wait for element state
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username_field = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "username"))
)
username_field.send_keys("test")

login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "login"))
)
login_button.click()
```

### 5. Hardcoded Locators in Step Definitions

**❌ NEVER put locators directly in step definitions:**

```python
# ❌ BAD: Locators in step definitions violate Page Object Model
@when('User enters "{username}" username')
def step_enter_username(context, username):
    driver = context.driver
    driver.find_element(By.NAME, "login").send_keys(username)  # BAD
```

**✅ ALWAYS use page objects:**

```python
# ✅ GOOD: Locators encapsulated in page objects
@when('User enters "{username}" username')
def step_enter_username(context, username):
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)  # Uses page object property
```

### 6. Overly Generic Exception Handling

**❌ NEVER catch generic Exception unless absolutely necessary:**

```python
# ❌ BAD: Catches everything including SystemExit, KeyboardInterrupt
try:
    driver.get(url)
except Exception:  # Too broad
    logger.error("Something went wrong")
```

**✅ ALWAYS catch specific exceptions:**

```python
# ✅ GOOD: Specific exceptions with appropriate handling
try:
    driver.get(url)
except TimeoutException as e:
    logger.error(f"Page load timeout: {url}")
    raise PageLoadError(f"Failed to load page: {url}") from e
except WebDriverException as e:
    logger.error(f"WebDriver error navigating to {url}: {e}")
    raise
```

### 7. Mutable Default Arguments

**❌ NEVER use mutable default arguments:**

```python
# ❌ BAD: Mutable default argument (shared between calls)
def add_user(name, roles=[]):  # BAD - list is mutable
    roles.append("user")
    return {"name": name, "roles": roles}
```

**✅ ALWAYS use None as default and create new instances:**

```python
# ✅ GOOD: None as default, create new list inside function
def add_user(name, roles=None):
    if roles is None:
        roles = []
    roles.append("user")
    return {"name": name, "roles": roles}
```

### 8. Unnecessary Complexity

**❌ NEVER write overly complex code when simple code works:**

```python
# ❌ BAD: Unnecessarily complex
result = True if condition == True else False

# ❌ BAD: Overly nested conditionals
if x:
    if y:
        if z:
            do_something()

# ❌ BAD: Complicated list comprehension
result = [item for sublist in [inner for inner in outer if condition1(inner)] 
          for item in sublist if condition2(item)]
```

**✅ ALWAYS prefer simple, readable code:**

```python
# ✅ GOOD: Simple and clear
result = condition

# ✅ GOOD: Early returns reduce nesting
if not x:
    return
if not y:
    return
if not z:
    return
do_something()

# ✅ GOOD: Break complex logic into steps
filtered_outer = [inner for inner in outer if condition1(inner)]
flattened = [item for sublist in filtered_outer for item in sublist]
result = [item for item in flattened if condition2(item)]
```

## Code Examples

This section demonstrates proper code style with before/after examples.

### Example 1: Driver Manager Method

**Before (Poor Style):**

```python
def getDriver():
    if not hasattr(_thread_local,'driver'):
        browser=ConfigReader().get_property("browser.type")
        if browser=="chrome":
            options=ChromeOptions()
            options.add_argument("--headless=new")
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    return _thread_local.driver
```

**After (Proper Style):**

```python
@classmethod
def get_driver(cls) -> WebDriver:
    """
    Get WebDriver instance for current thread with lazy initialization.

    Returns same driver instance for repeated calls within same thread.
    Creates new driver on first call per thread using _create_driver().

    Returns:
        WebDriver: Thread-local WebDriver instance (Chrome or Firefox)

    Raises:
        DriverInitializationError: If driver creation fails

    Example:
        >>> driver = DriverManager.get_driver()
        >>> driver.get("https://example.com")
    """
    # Check if current thread already has a driver instance
    if not hasattr(cls._thread_local, 'driver') or cls._thread_local.driver is None:
        thread_name = threading.current_thread().name
        logger.info(
            "No WebDriver found for thread '%s', initializing new instance",
            thread_name
        )
        
        try:
            # Create new driver for this thread
            cls._thread_local.driver = cls._create_driver()
            logger.info(
                "Successfully initialized WebDriver for thread '%s'",
                thread_name
            )
        except Exception as e:
            logger.exception(
                "Failed to initialize WebDriver for thread '%s': %s",
                thread_name,
                e
            )
            raise DriverInitializationError(
                f"WebDriver initialization failed for thread '{thread_name}': {e}"
            ) from e
    
    return cls._thread_local.driver
```

**Key Improvements:**
- ✅ Comprehensive docstring with Args, Returns, Raises, Example
- ✅ Proper formatting (Black-compatible)
- ✅ Type hints on return value
- ✅ snake_case naming (`get_driver` not `getDriver`)
- ✅ Logging instead of silent execution
- ✅ Proper exception handling with custom exception
- ✅ Clear comments explaining critical patterns
- ✅ Proper spacing and indentation

### Example 2: Page Object Method

**Before (Poor Style):**

```python
def login(self,username,password):
    self.driver.find_element(By.NAME,"login").send_keys(username)
    self.driver.find_element(By.NAME,"password").send_keys(password)
    self.driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
```

**After (Proper Style):**

```python
def login(self, username: str, password: str) -> None:
    """
    Perform login with provided credentials.

    Enters username and password into login form fields and clicks
    the login button. Uses property-based element access with explicit
    waits to ensure elements are ready before interaction.

    Args:
        username (str): Email address or username for authentication
        password (str): Password for authentication

    Raises:
        TimeoutException: If login form elements not found within timeout
        WebDriverException: If interaction with form elements fails

    Example:
        >>> login_page = LoginPage(driver)
        >>> login_page.login("user@example.com", "password123")
        >>> # User should now be on dashboard
    """
    logger.info("Attempting login with username: %s", username)
    
    # Enter credentials using property-based element access
    # Properties handle waits and element refresh automatically
    self.input_email.send_keys(username)
    self.input_password.send_keys(password)
    
    # Click login button
    self.login_button.click()
    
    logger.info("Login form submitted for username: %s", username)
```

**Key Improvements:**
- ✅ Comprehensive docstring
- ✅ Type hints for parameters and return value
- ✅ Uses property-based element access (not direct find_element)
- ✅ Proper spacing around commas and parentheses
- ✅ Logging for debugging
- ✅ Clear comments explaining approach
- ✅ Documents raised exceptions

### Example 3: Step Definition

**Before (Poor Style):**

```python
@given('User is on the upgenix login page')
def navigate_to_login(context):
    url=ConfigReader().get_property("web.table.url")
    context.driver.get(url)
```

**After (Proper Style):**

```python
@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """
    Navigate to login page using configured URL from config.yaml.

    This step implements the Background step from Login.feature, executed before
    each scenario to ensure user starts on the login page.

    Configuration:
        Retrieves login URL from config.yaml via ConfigReader.get_property('web.table.url').

    Args:
        context: Behave context object containing driver and configuration
                context.driver: WebDriver instance for browser navigation

    Raises:
        KeyError: If 'web.table.url' configuration key missing
        WebDriverException: If navigation to URL fails

    Example:
        Given User is on the upgenix login page
        # Browser navigates to https://testinium.example.com/login
    """
    config = ConfigReader()
    url = config.get_property("web.table.url")
    
    logger.info("Navigating to login page: %s", url)
    context.driver.get(url)
    logger.info("Successfully navigated to login page")
```

**Key Improvements:**
- ✅ Function name has `step_` prefix for clarity
- ✅ Comprehensive docstring with Gherkin example
- ✅ Proper spacing
- ✅ Logging for test execution visibility
- ✅ Clear variable names
- ✅ Documents raised exceptions

### Example 4: Configuration Class

**Before (Poor Style):**

```python
class Config:
    def __init__(self):
        self.timeout=10
        self.browser="chrome"
        self.headless=False
```

**After (Proper Style):**

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class BrowserConfig:
    """
    Browser configuration settings.

    Attributes:
        type (str): Browser type ('chrome' or 'firefox'). Defaults to 'chrome'.
        headless (bool): Run browser in headless mode. Defaults to False.
        window_size (Optional[tuple]): Browser window size (width, height).
            Defaults to None (maximized window).
    """
    type: str = "chrome"
    headless: bool = False
    window_size: Optional[tuple[int, int]] = None


@dataclass
class TimeoutConfig:
    """
    Timeout configuration settings.

    Attributes:
        explicit (int): Explicit wait timeout in seconds. Defaults to 10.
        page_load (int): Page load timeout in seconds. Defaults to 30.
        script (int): Script execution timeout in seconds. Defaults to 30.
    """
    explicit: int = 10
    page_load: int = 30
    script: int = 30


@dataclass
class Config:
    """
    Main configuration container.

    Attributes:
        browser (BrowserConfig): Browser-specific configuration
        timeout (TimeoutConfig): Timeout-related configuration
    """
    browser: BrowserConfig
    timeout: TimeoutConfig
```

**Key Improvements:**
- ✅ Uses dataclasses for clean structure
- ✅ Type hints on all attributes
- ✅ Comprehensive docstrings
- ✅ Grouped related settings into sub-configurations
- ✅ Default values explicitly defined
- ✅ Optional types where applicable

## See Also

- [Development Setup Guide](development-setup.md) - Setting up your development environment
- [Testing Guidelines](testing-guidelines.md) - Writing and running tests
- [Documentation Guidelines](documentation-guidelines.md) - Writing documentation
- [Pull Request Process](pull-request-process.md) - Contributing code changes

## References

- **PEP 8:** https://www.python.org/dev/peps/pep-0008/
- **PEP 257 (Docstring Conventions):** https://www.python.org/dev/peps/pep-0257/
- **Black Documentation:** https://black.readthedocs.io/
- **isort Documentation:** https://pycqa.github.io/isort/
- **mypy Documentation:** http://mypy-lang.org/
- **Google Python Style Guide:** https://google.github.io/styleguide/pyguide.html
- **Agent Action Plan Section 0.9:** Documentation-Specific Instructions

---

**Last Updated:** 2024-01-15  
**Maintained By:** Testinium QA Team  
**Version:** 1.0.0
