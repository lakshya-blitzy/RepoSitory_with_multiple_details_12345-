# Screenshot Helper API Reference

## Module Overview

The `screenshot_helper` module provides essential utilities for capturing screenshots and browser console logs during test execution failures. These functions enable comprehensive failure diagnostics by preserving visual evidence and browser state information.

**Module:** `utilities.screenshot_helper`

**Purpose:** Test failure diagnostics through automated screenshot capture and browser log collection

**Key Features:**
- Automatic screenshot capture with WebDriver
- Cross-platform filename sanitization
- Timestamp-based unique file naming
- File system storage in `reports/screenshots/` directory
- Optional Allure report integration
- Browser console log capture for JavaScript errors and warnings
- Comprehensive error handling and logging

**Migration Context:**

This module extracts and enhances screenshot capture logic from the original Java `Hooks.java` `@After` annotation, providing reusable Python functions with improved error handling, optional Allure integration, and browser log capture capabilities not present in the original implementation.

**Original Java Source:** `src/main/java/com/testinium/step_definitions/Hooks.java`

**Source:** `utilities/screenshot_helper.py`

---

## Functions

### sanitize_filename()

```python
def sanitize_filename(filename: str) -> str
```

Sanitize filename by removing or replacing invalid filesystem characters for cross-platform compatibility.

**Description:**

Removes characters that are invalid in filenames across Windows, Linux, and macOS operating systems. This ensures screenshot and log files can be created reliably regardless of the test scenario name used.

Invalid characters removed or replaced:
- Forward slashes (`/`)
- Backslashes (`\`)
- Colons (`:`)
- Asterisks (`*`)
- Question marks (`?`)
- Double quotes (`"`)
- Less than (`<`)
- Greater than (`>`)
- Pipe (`|`)

Additionally replaces spaces with underscores for better command-line compatibility and limits filename length to 200 characters.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filename` | `str` | Yes | Original filename string to sanitize |

**Returns:**

| Type | Description |
|------|-------------|
| `str` | Sanitized filename safe for cross-platform filesystem operations |

**Example:**

```python
from utilities.screenshot_helper import sanitize_filename

# Sanitize scenario name with special characters
original_name = "User login: admin@example.com"
safe_name = sanitize_filename(original_name)
print(safe_name)
# Output: 'User_login_admin_example_com'

# Sanitize filename with path separators
test_case = "CRM/Sales/Create Order"
safe_test = sanitize_filename(test_case)
print(safe_test)
# Output: 'CRM_Sales_Create_Order'

# Handle empty results after sanitization
invalid_only = ":::"
safe_invalid = sanitize_filename(invalid_only)
print(safe_invalid)
# Output: 'screenshot' (default fallback)
```

**Implementation Details:**

- Uses regular expression pattern `[<>:"/\\|?*]` to match invalid characters
- Strips leading/trailing underscores and dots after sanitization
- Returns `'screenshot'` as fallback if sanitized string is empty
- Maximum length: 200 characters (leaving room for timestamp and extension)

**Source:** `utilities/screenshot_helper.py:46-94`

---

### capture_screenshot()

```python
def capture_screenshot(
    driver: WebDriver,
    scenario_name: str,
    attach_to_allure: bool = True
) -> Optional[str]
```

Capture screenshot from Selenium WebDriver instance and save to filesystem with optional Allure report integration.

**Description:**

This function provides comprehensive screenshot capture functionality for test failure diagnostics. It extracts the screenshot capture logic from the original Java `Hooks.java` `@After` method and enhances it with:

- File system storage for persistent screenshot archives
- Automatic timestamp generation for unique filenames
- Cross-platform filename sanitization
- Optional Allure report attachment
- Comprehensive error handling and logging

The function creates the `reports/screenshots/` directory if it doesn't exist and saves screenshots with the naming pattern: `{scenario_name}_{timestamp}.png`

**Original Java Implementation:**

```java
// Hooks.java lines 14-15
byte[] screenshot = ((TakesScreenshot) Driver.getDriver())
                   .getScreenshotAs(OutputType.BYTES);
scenario.attach(screenshot, "image/png", scenario.getName());
```

**Python Enhancement:**
- Adds file system storage beyond report attachment
- Implements automatic timestamp generation
- Provides cross-platform filename sanitization
- Includes comprehensive error handling
- Supports optional Allure integration

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `driver` | `WebDriver` | Yes | - | Selenium WebDriver instance for screenshot capture |
| `scenario_name` | `str` | Yes | - | Name of the test scenario (used in filename) |
| `attach_to_allure` | `bool` | No | `True` | Whether to attach screenshot to Allure report |

**Returns:**

| Type | Description |
|------|-------------|
| `Optional[str]` | Absolute path to saved screenshot file on success, `None` on failure |

**Error Handling:**

This function does not raise exceptions. Instead, it logs errors and returns `None` on failure, allowing test execution to continue even if screenshot capture fails.

**Example:**

```python
from selenium import webdriver
from utilities.screenshot_helper import capture_screenshot

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Navigate and perform test actions
    driver.get("https://example.com")
    # ... test logic ...
    
    # Capture screenshot on failure
    screenshot_path = capture_screenshot(
        driver=driver,
        scenario_name="Login Test Failed",
        attach_to_allure=True
    )
    
    if screenshot_path:
        print(f"Screenshot saved to: {screenshot_path}")
        # Output: Screenshot saved to: /path/to/reports/screenshots/Login_Test_Failed_20240115_143022.png
    else:
        print("Screenshot capture failed")
        
finally:
    driver.quit()
```

**Usage in Behave Hooks:**

```python
# features/environment.py
from utilities.screenshot_helper import capture_screenshot
from utilities.driver_manager import DriverManager

def after_scenario(context, scenario):
    """Capture screenshot on scenario failure."""
    if scenario.status == 'failed':
        driver = DriverManager.get_driver()
        screenshot_path = capture_screenshot(
            driver=driver,
            scenario_name=scenario.name,
            attach_to_allure=True
        )
        if screenshot_path:
            print(f"\n📸 Screenshot: {screenshot_path}")
```

**Filename Format:**

```
{sanitized_scenario_name}_{YYYYMMDD}_{HHMMSS}.png
```

Example: `User_Login_Test_20240115_143022.png`

**Storage Location:**

```
reports/
└── screenshots/
    ├── Login_Test_Failed_20240115_143022.png
    ├── CRM_Create_Order_20240115_143145.png
    └── Inventory_Search_20240115_143230.png
```

**Allure Integration:**

When `attach_to_allure=True` and `allure-behave` is installed:
- Screenshot is attached to Allure report as PNG attachment
- Attachment name uses sanitized scenario name
- Failure is logged (not raised) if Allure attachment fails

**Source:** `utilities/screenshot_helper.py:97-191`

---

### capture_browser_logs()

```python
def capture_browser_logs(
    driver: WebDriver,
    scenario_name: str,
    log_types: Optional[List[str]] = None
) -> Optional[Dict[str, List[str]]]
```

Capture browser console logs for comprehensive test failure diagnostics.

**Description:**

This function provides enhanced debugging capabilities by capturing browser console logs including JavaScript errors, warnings, and network issues. This enhancement goes beyond the original Java implementation by preserving browser state information that can help diagnose test failures.

The function captures multiple log types (browser, driver, performance), saves them to the filesystem for persistent analysis, and provides structured log data for programmatic processing.

**Enhancement over Java Implementation:**

The original Java `Hooks.java` only captured screenshots. This Python implementation adds:
- Multiple log type capture (browser, driver, client, server, performance)
- Persistent filesystem storage for analysis
- Structured log data for programmatic processing
- Optional Allure report integration for log visualization

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `driver` | `WebDriver` | Yes | - | Selenium WebDriver instance for log retrieval |
| `scenario_name` | `str` | Yes | - | Name of the test scenario (used in log filename) |
| `log_types` | `Optional[List[str]]` | No | `['browser']` | List of log types to capture |

**Valid Log Types:**

- `'browser'` - Browser console logs (JavaScript errors, warnings, info)
- `'driver'` - WebDriver command logs
- `'client'` - Client-side logs
- `'server'` - Server-side logs
- `'performance'` - Performance timing logs

**Returns:**

| Type | Description |
|------|-------------|
| `Optional[Dict[str, List[str]]]` | Dictionary mapping log type to list of log entry strings on success, `None` on failure |

**Return Value Structure:**

```python
{
    'browser': [
        '[SEVERE] Uncaught TypeError: Cannot read property...',
        '[WARNING] Resource loading failed: /api/data',
        '[INFO] User interaction logged'
    ],
    'driver': [
        '[INFO] WebDriver command: navigate to https://example.com'
    ]
}
```

**Error Handling:**

This function does not raise exceptions. It logs warnings for unavailable log types and returns `None` on complete failure.

**Example:**

```python
from selenium import webdriver
from utilities.screenshot_helper import capture_browser_logs

# Initialize WebDriver with logging enabled
options = webdriver.ChromeOptions()
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
driver = webdriver.Chrome(options=options)

try:
    # Navigate and perform test
    driver.get("https://example.com")
    # ... test actions that might trigger console errors ...
    
    # Capture browser logs on failure
    logs = capture_browser_logs(
        driver=driver,
        scenario_name="Login Test Failed",
        log_types=['browser', 'performance']
    )
    
    if logs:
        # Process captured logs
        print(f"Captured {len(logs)} log types")
        
        if 'browser' in logs:
            print(f"\nBrowser console logs ({len(logs['browser'])} entries):")
            for log_entry in logs['browser']:
                if 'SEVERE' in log_entry:
                    print(f"  ERROR: {log_entry}")
                    
        # Output:
        # Captured 2 log types
        #
        # Browser console logs (5 entries):
        #   ERROR: [SEVERE] Uncaught TypeError: Cannot read property 'value' of null
    else:
        print("No logs captured")
        
finally:
    driver.quit()
```

**Usage in Behave Hooks:**

```python
# features/environment.py
from utilities.screenshot_helper import capture_screenshot, capture_browser_logs
from utilities.driver_manager import DriverManager

def after_scenario(context, scenario):
    """Capture screenshot and logs on scenario failure."""
    if scenario.status == 'failed':
        driver = DriverManager.get_driver()
        
        # Capture screenshot
        screenshot_path = capture_screenshot(driver, scenario.name)
        
        # Capture browser console logs
        logs = capture_browser_logs(
            driver=driver,
            scenario_name=scenario.name,
            log_types=['browser', 'driver']
        )
        
        # Report diagnostics
        if screenshot_path:
            print(f"\n📸 Screenshot: {screenshot_path}")
        if logs:
            error_count = sum(1 for entry in logs.get('browser', []) if 'SEVERE' in entry)
            print(f"🔍 Browser logs captured: {error_count} errors found")
```

**Log File Format:**

Captured logs are saved with the filename pattern:
```
{sanitized_scenario_name}_{YYYYMMDD}_{HHMMSS}_logs.txt
```

Example log file content:
```
Browser Logs for Scenario: Login Test Failed
Captured at: 2024-01-15T14:30:22.123456
================================================================================

[BROWSER LOGS]
--------------------------------------------------------------------------------
[SEVERE] Uncaught TypeError: Cannot read property 'value' of null
    at LoginPage.submitForm (login.js:45)
[WARNING] Resource failed to load: /api/user/profile
[INFO] User session initialized

[DRIVER LOGS]
--------------------------------------------------------------------------------
[INFO] WebDriver command: navigate to https://example.com/login
[INFO] WebDriver command: findElement By.name: username
```

**Storage Location:**

```
reports/
└── screenshots/
    ├── Login_Test_Failed_20240115_143022.png
    ├── Login_Test_Failed_20240115_143022_logs.txt
    └── ...
```

**Allure Integration:**

When `allure-behave` is installed:
- Logs are automatically attached to Allure report as text attachments
- Attachment name format: `{sanitized_scenario_name}_browser_logs`
- Visible in Allure report under test failure details

**Platform Compatibility:**

Log availability varies by browser and driver:
- **Chrome/ChromeDriver**: Full browser console log support
- **Firefox/GeckoDriver**: Limited browser log support (driver logs available)
- **Safari/SafariDriver**: Minimal log support
- **Edge/EdgeDriver**: Similar to Chrome support

The function gracefully handles unavailable log types by logging warnings and continuing with available types.

**Source:** `utilities/screenshot_helper.py:194-320`

---

### take_screenshot()

```python
def take_screenshot(
    driver: WebDriver,
    name: str = "screenshot"
) -> Optional[str]
```

Convenience wrapper for `capture_screenshot()` with simplified interface and no Allure integration.

**Description:**

This is a simplified convenience function for quick screenshot capture without Allure report integration. Useful for manual debugging or situations where Allure reports are not used.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `driver` | `WebDriver` | Yes | - | Selenium WebDriver instance |
| `name` | `str` | No | `"screenshot"` | Simple name for the screenshot |

**Returns:**

| Type | Description |
|------|-------------|
| `Optional[str]` | Path to saved screenshot or `None` on failure |

**Example:**

```python
from selenium import webdriver
from utilities.screenshot_helper import take_screenshot

driver = webdriver.Chrome()
driver.get("https://example.com")

# Quick screenshot with default name
screenshot_path = take_screenshot(driver)
# Saved as: reports/screenshots/screenshot_20240115_143022.png

# Screenshot with custom name
custom_path = take_screenshot(driver, "homepage_view")
# Saved as: reports/screenshots/homepage_view_20240115_143045.png

driver.quit()
```

**Source:** `utilities/screenshot_helper.py:324-335`

---

## Migration Notes

### Java to Python Transformation

**Original Java Implementation (Hooks.java):**

```java
@After
public void tearDown(Scenario scenario) {
    if (scenario.isFailed()) {
        byte[] screenshot = ((TakesScreenshot) Driver.getDriver())
                           .getScreenshotAs(OutputType.BYTES);
        scenario.attach(screenshot, "image/png", scenario.getName());
    }
    Driver.quit();
}
```

**Python Enhancement:**

```python
# features/environment.py
def after_scenario(context, scenario):
    """Enhanced teardown with screenshot and log capture."""
    if scenario.status == 'failed':
        driver = DriverManager.get_driver()
        
        # Capture screenshot with filesystem storage
        capture_screenshot(driver, scenario.name, attach_to_allure=True)
        
        # NEW: Capture browser logs for diagnostics
        capture_browser_logs(driver, scenario.name)
    
    DriverManager.quit_driver()
```

**Key Differences:**

1. **Reusable Functions**: Extracted from hook into dedicated module functions
2. **File System Storage**: Screenshots saved to disk, not just attached to reports
3. **Browser Log Capture**: New capability not in original Java implementation
4. **Comprehensive Error Handling**: Functions log errors instead of crashing tests
5. **Filename Sanitization**: Cross-platform safe filenames with timestamps
6. **Optional Allure Integration**: Controlled via parameter, not hardcoded

---

## Usage Patterns

### Pattern 1: Behave Hook Integration

Most common usage pattern for automatic failure diagnostics:

```python
# features/environment.py
from utilities.screenshot_helper import capture_screenshot, capture_browser_logs
from utilities.driver_manager import DriverManager

def after_scenario(context, scenario):
    """Capture diagnostics on test failure."""
    if scenario.status == 'failed':
        driver = DriverManager.get_driver()
        
        # Capture screenshot
        screenshot_path = capture_screenshot(driver, scenario.name)
        
        # Capture browser logs
        logs = capture_browser_logs(driver, scenario.name)
        
        # Attach to context for access in steps
        context.failure_screenshot = screenshot_path
        context.failure_logs = logs
    
    # Cleanup
    DriverManager.quit_driver()
```

### Pattern 2: Manual Screenshot Capture in Steps

Capture screenshots at specific points during test execution:

```python
# features/steps/crm_steps.py
from behave import when, then
from utilities.screenshot_helper import capture_screenshot
from utilities.driver_manager import DriverManager

@when('I create a new customer record')
def step_create_customer(context):
    driver = DriverManager.get_driver()
    # ... create customer logic ...
    
    # Capture evidence of successful creation
    capture_screenshot(
        driver=driver,
        scenario_name="Customer Created",
        attach_to_allure=True
    )

@then('the customer appears in the CRM list')
def step_verify_customer(context):
    driver = DriverManager.get_driver()
    # ... verification logic ...
    
    # Capture screenshot for documentation
    capture_screenshot(driver, "Customer Verification")
```

### Pattern 3: Conditional Log Capture

Capture browser logs only when errors are detected:

```python
from selenium import webdriver
from utilities.screenshot_helper import capture_browser_logs

driver = webdriver.Chrome()
driver.get("https://example.com")

# Perform test actions
# ...

# Check for browser errors
logs = capture_browser_logs(driver, "Initial Page Load", log_types=['browser'])

if logs and 'browser' in logs:
    errors = [entry for entry in logs['browser'] if 'SEVERE' in entry]
    if errors:
        print(f"⚠️  {len(errors)} JavaScript errors detected:")
        for error in errors:
            print(f"  {error}")
```

### Pattern 4: Comprehensive Diagnostics Function

Create a helper function for complete failure diagnostics:

```python
from typing import Tuple, Optional, Dict, List
from selenium.webdriver.remote.webdriver import WebDriver
from utilities.screenshot_helper import capture_screenshot, capture_browser_logs

def capture_failure_diagnostics(
    driver: WebDriver,
    scenario_name: str
) -> Tuple[Optional[str], Optional[Dict[str, List[str]]]]:
    """
    Capture both screenshot and logs for comprehensive diagnostics.
    
    Args:
        driver: WebDriver instance
        scenario_name: Name of failed scenario
    
    Returns:
        Tuple of (screenshot_path, captured_logs)
    """
    screenshot_path = capture_screenshot(
        driver=driver,
        scenario_name=scenario_name,
        attach_to_allure=True
    )
    
    logs = capture_browser_logs(
        driver=driver,
        scenario_name=scenario_name,
        log_types=['browser', 'driver', 'performance']
    )
    
    return screenshot_path, logs

# Usage in hook
def after_scenario(context, scenario):
    if scenario.status == 'failed':
        driver = DriverManager.get_driver()
        screenshot, logs = capture_failure_diagnostics(driver, scenario.name)
        
        # Report summary
        if screenshot:
            print(f"\n📸 Screenshot captured: {screenshot}")
        if logs:
            total_entries = sum(len(entries) for entries in logs.values())
            print(f"🔍 Logs captured: {total_entries} entries across {len(logs)} types")
```

---

## Thread Safety

The screenshot helper functions are **thread-safe** when used with thread-local WebDriver instances from `DriverManager.get_driver()`.

**Thread Safety Guarantees:**

- ✅ **File I/O**: Each function creates unique timestamped filenames, preventing race conditions
- ✅ **WebDriver Access**: Functions accept WebDriver as parameter; thread safety depends on caller using thread-local drivers
- ✅ **Directory Creation**: `Path.mkdir(parents=True, exist_ok=True)` is thread-safe
- ✅ **Logging**: Python's logging module is thread-safe

**Parallel Execution Usage:**

```python
# Safe for parallel execution with behave-parallel or pytest-xdist
from utilities.screenshot_helper import capture_screenshot
from utilities.driver_manager import DriverManager

def after_scenario(context, scenario):
    """Thread-safe failure diagnostics."""
    if scenario.status == 'failed':
        # Each thread has its own WebDriver instance
        driver = DriverManager.get_driver()  # Thread-local
        
        # Unique timestamped filename prevents conflicts
        capture_screenshot(driver, scenario.name)
```

---

## Troubleshooting

### Issue: Screenshot Capture Returns None

**Symptoms:**
- `capture_screenshot()` returns `None`
- No screenshot file created
- Error in logs: "Cannot capture screenshot: WebDriver instance is None"

**Causes:**
1. WebDriver instance is `None` or not properly initialized
2. WebDriver session has already terminated
3. Browser window has been closed

**Solutions:**

```python
# Verify WebDriver is active before capturing
from utilities.driver_manager import DriverManager

driver = DriverManager.get_driver()

# Check driver is not None
if driver is None:
    print("ERROR: WebDriver not initialized")
else:
    # Check driver session is active
    try:
        driver.current_url  # Will raise if session terminated
        screenshot = capture_screenshot(driver, "test")
    except Exception as e:
        print(f"WebDriver session invalid: {e}")
```

### Issue: Browser Logs Not Captured

**Symptoms:**
- `capture_browser_logs()` returns empty dictionary or `None`
- Warning in logs: "Log type 'browser' not available"

**Causes:**
1. Browser doesn't support requested log type
2. Browser logging not enabled in WebDriver capabilities
3. GeckoDriver (Firefox) has limited log support

**Solutions:**

```python
from selenium import webdriver

# Enable browser logging for Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
driver = webdriver.Chrome(options=chrome_options)

# Check available log types
available_types = driver.log_types
print(f"Available log types: {available_types}")

# Request only available types
logs = capture_browser_logs(driver, "test", log_types=['browser'])
```

### Issue: Allure Attachment Fails

**Symptoms:**
- Screenshot saved to filesystem but not in Allure report
- Warning: "Allure integration requested but allure-behave not installed"

**Causes:**
1. `allure-behave` package not installed
2. Allure report generation not configured
3. `attach_to_allure=True` but running outside Allure context

**Solutions:**

```bash
# Install allure-behave
pip install allure-behave

# Run tests with Allure formatter
behave --format=allure_behave.formatter:AllureFormatter \
       -o allure-results
```

```python
# Disable Allure attachment if not using Allure
screenshot = capture_screenshot(
    driver=driver,
    scenario_name="test",
    attach_to_allure=False  # Disable Allure integration
)
```

### Issue: Permission Denied Creating Screenshot Directory

**Symptoms:**
- Error: "Permission denied: 'reports/screenshots'"
- Screenshot capture returns `None`

**Causes:**
1. Insufficient file system permissions
2. Running from read-only directory
3. Directory owned by different user

**Solutions:**

```bash
# Verify write permissions
ls -la reports/

# Create directory with correct permissions
mkdir -p reports/screenshots
chmod 755 reports/screenshots

# Run tests with appropriate user permissions
```

---

## See Also

### Related API Documentation

- **[Driver Manager API](driver-manager.md)** - WebDriver lifecycle management for screenshot capture
- **[Wait Helpers API](wait-helpers.md)** - Wait strategies before capturing diagnostic screenshots
- **[Config Reader API](config-reader.md)** - Configuration for screenshot storage paths

### Related Guides

- **[Screenshot Management Guide](../../guides/screenshot-management.md)** - Best practices for screenshot capture
- **[Parallel Execution Guide](../../guides/parallel-execution.md)** - Thread-safe screenshot capture
- **[Custom Reporters Guide](../../guides/custom-reporters.md)** - Integrating screenshots with custom reports

### External Documentation

- **[Selenium WebDriver Screenshots](https://www.selenium.dev/documentation/webdriver/interactions/windows/#takescreenshot)** - Official Selenium screenshot documentation
- **[Allure Report Integration](https://docs.qameta.io/allure/)** - Allure attachment documentation
- **[Python Pathlib](https://docs.python.org/3/library/pathlib.html)** - Path manipulation for screenshot storage

---

**Last Updated:** Auto-generated from source code  
**Module Version:** 1.0.0  
**Python Compatibility:** 3.9+
